#!/usr/bin/env python

"""
This module implements row model of MUFG bank CSV.
"""

from __future__ import annotations
from abc import abstractmethod
import datetime
from enum import Enum
from typing import Union
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_row import AccountRow, AccountRowData
from zaimcsvconverter.enum import Account
from zaimcsvconverter.models import Store
from zaimcsvconverter.zaim.zaim_row import ZaimTransferRow, ZaimIncomeRow, ZaimPaymentRow


class CashFlowKind(Enum):
    """
    This class implements constant of cash flow kind in MUFG CSV.
    """
    INCOME: str = '入金'
    PAYMENT: str = '支払い'
    TRANSFER_INCOME: str = '振替入金'
    TRANSFER_PAYMENT: str = '振替支払い'


@dataclass
class MufgRowData(AccountRowData):
    """This class implements data class for wrapping list of MUFG bunk CSV row model."""
    date: str
    summary: str
    summary_content: str
    payed_amount: str
    deposit_amount: str
    balance: str
    note: str
    is_uncapitalized: str
    cash_flow_kind: str


# pylint: disable=too-many-instance-attributes
class MufgRow(AccountRow):
    """
    This class implements row model of MUFG bank CSV.
    """
    def __init__(self, list_row_waon: MufgRowData):
        self._date: datetime = datetime.datetime.strptime(list_row_waon.date, "%Y/%m/%d")
        self._summary: str = list_row_waon.summary
        self._summary_content: Store = Store.try_to_find(Account.MUFG, list_row_waon.summary_content)
        self._payed_amount: int = self._convert_string_to_int_or_none(list_row_waon.payed_amount)
        self._deposit_amount: int = self._convert_string_to_int_or_none(list_row_waon.deposit_amount)
        self._balance = int(list_row_waon.balance.replace(',', ''))
        self._note: str = list_row_waon.note
        self._is_uncapitalized: str = list_row_waon.is_uncapitalized

    @staticmethod
    def _convert_string_to_int_or_none(string) -> Union[int, None]:
        if string == '':
            return None
        return int(string.replace(',', ''))

    @property
    @abstractmethod
    def _cash_flow_source_on_zaim(self) -> str:
        pass

    @property
    @abstractmethod
    def _cash_flow_target_on_zaim(self) -> str:
        pass

    @property
    @abstractmethod
    def _amount(self) -> int:
        pass

    @property
    def zaim_date(self) -> datetime:
        return self._date

    @property
    def zaim_store(self) -> Store:
        return self._summary_content

    @property
    def zaim_income_cash_flow_target(self) -> str:
        return self._cash_flow_target_on_zaim

    @property
    def zaim_income_ammount_income(self) -> int:
        return self._amount

    @property
    def zaim_payment_cash_flow_source(self) -> str:
        return self._cash_flow_source_on_zaim

    @property
    def zaim_payment_amount_payment(self) -> int:
        return self._amount

    @property
    def zaim_transfer_cash_flow_source(self) -> str:
        return self._cash_flow_source_on_zaim

    @property
    def zaim_transfer_cash_flow_target(self) -> str:
        return self._cash_flow_target_on_zaim

    @property
    def zaim_transfer_amount_transfer(self) -> int:
        return self._amount

    @staticmethod
    def create(row_data: MufgRowData) -> MufgRow:
        try:
            cash_flow_kind = CashFlowKind(row_data.cash_flow_kind)
        except ValueError as error:
            raise NotImplementedError(
                'The value of "Cash flow kind" has not been defined in this code. Cash flow kind ='
                + row_data.cash_flow_kind
            ) from error

        return {
            CashFlowKind.INCOME: MufgIncomeRow(row_data),
            CashFlowKind.PAYMENT: MufgPaymentRow(row_data),
            CashFlowKind.TRANSFER_INCOME: MufgTransferIncomeRow(row_data),
            CashFlowKind.TRANSFER_PAYMENT: MufgTransferPaymentRow(row_data)
        }.get(cash_flow_kind)


class MufgAbstractIncomeRow(MufgRow):
    """
    This class implements abstract income row model of MUFG bank CSV.
    """
    @abstractmethod
    def convert_to_zaim_row(self):
        pass

    @property
    @abstractmethod
    def _cash_flow_source_on_zaim(self) -> str:
        pass

    @property
    def _cash_flow_target_on_zaim(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def _amount(self) -> int:
        return self._deposit_amount


class MufgAbstractPaymentRow(MufgRow):
    """
    This class implements abstract payment row model of MUFG bank CSV.
    """
    @abstractmethod
    def convert_to_zaim_row(self):
        pass

    @property
    def _cash_flow_source_on_zaim(self) -> str:
        return CONFIG.mufg.account_name

    @property
    @abstractmethod
    def _cash_flow_target_on_zaim(self) -> str:
        pass

    @property
    def _amount(self) -> int:
        return self._payed_amount


class MufgIncomeRow(MufgAbstractIncomeRow):
    """
    This class implements income row model of MUFG bank CSV.
    """
    def convert_to_zaim_row(self):
        return ZaimTransferRow(self)

    @property
    def _cash_flow_source_on_zaim(self) -> str:
        return CONFIG.mufg.transfer_account_name


class MufgPaymentRow(MufgAbstractPaymentRow):
    """
    This class implements payment row model of MUFG bank CSV.
    """
    def convert_to_zaim_row(self):
        return ZaimTransferRow(self)

    @property
    def _cash_flow_target_on_zaim(self) -> str:
        return CONFIG.mufg.transfer_account_name


class MufgTransferIncomeRow(MufgAbstractIncomeRow):
    """
    This class implements transfer income row model of MUFG bank CSV.
    """
    def convert_to_zaim_row(self):
        if self._summary_content.transfer_target is None:
            return ZaimIncomeRow(self)
        return ZaimTransferRow(self)

    @property
    def _cash_flow_source_on_zaim(self) -> str:
        return self._summary_content.transfer_target


class MufgTransferPaymentRow(MufgAbstractPaymentRow):
    """
    This class implements transfer payment row model of MUFG bank CSV.
    """
    def convert_to_zaim_row(self):
        if self._summary_content.transfer_target is None:
            return ZaimPaymentRow(self)
        return ZaimTransferRow(self)

    @property
    def _cash_flow_target_on_zaim(self) -> str:
        return self._summary_content.transfer_target
