#!/usr/bin/env python

"""
This module implements row model of MUFG bank CSV.
"""

from __future__ import annotations
from abc import abstractmethod
import datetime
from enum import Enum
from typing import Union, TYPE_CHECKING
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_row import AccountRow, AccountStoreRowData, AccountRowFactory
from zaimcsvconverter.models import Store
from zaimcsvconverter.unility import Utility
from zaimcsvconverter.zaim_row import ZaimTransferRow, ZaimIncomeRow, ZaimPaymentRow
if TYPE_CHECKING:
    from zaimcsvconverter.account import Account


class CashFlowKind(Enum):
    """
    This class implements constant of cash flow kind in MUFG CSV.
    """
    INCOME: str = '入金'
    PAYMENT: str = '支払い'
    TRANSFER_INCOME: str = '振替入金'
    TRANSFER_PAYMENT: str = '振替支払い'


class MufgRowFactory(AccountRowFactory):
    """This class implements factory to create MUFG CSV row instance."""
    def create(self, account: 'Account', row_data: MufgRowData) -> MufgRow:
        try:
            cash_flow_kind = CashFlowKind(row_data.cash_flow_kind)
        except ValueError as error:
            raise NotImplementedError(
                'The value of "Cash flow kind" has not been defined in this code. Cash flow kind ='
                + row_data.cash_flow_kind
            ) from error

        mufg_row_class = {
            CashFlowKind.INCOME: MufgIncomeRow,
            CashFlowKind.PAYMENT: MufgPaymentRow,
            CashFlowKind.TRANSFER_INCOME: MufgTransferIncomeRow,
            CashFlowKind.TRANSFER_PAYMENT: MufgTransferPaymentRow,
        }.get(cash_flow_kind)

        return mufg_row_class(account, row_data)


@dataclass
class MufgRowData(AccountStoreRowData):
    """This class implements data class for wrapping list of MUFG bunk CSV row model."""
    _date: str
    summary: str
    _summary_content: str
    payed_amount: str
    deposit_amount: str
    balance: str
    note: str
    is_uncapitalized: str
    cash_flow_kind: str

    @property
    def date(self) -> datetime:
        """This property returns date as datetime."""
        return datetime.datetime.strptime(self._date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        """This property returns store name."""
        return self._summary_content


# pylint: disable=too-many-instance-attributes
class MufgRow(AccountRow):
    """
    This class implements row model of MUFG bank CSV.
    """
    def __init__(self, account: 'Account', row_data: MufgRowData):
        super().__init__(account)
        self._date: datetime = row_data.date
        self._summary: str = row_data.summary
        self._summary_content: Store = self.try_to_find_store(row_data.store_name)
        self._payed_amount: int = Utility.convert_string_to_int_or_none(row_data.payed_amount)
        self._deposit_amount: int = Utility.convert_string_to_int_or_none(row_data.deposit_amount)
        self._balance = int(row_data.balance.replace(',', ''))
        self._note: str = row_data.note
        self._is_uncapitalized: str = row_data.is_uncapitalized

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


class MufgAbstractIncomeRow(MufgRow):
    """
    This class implements abstract income row model of MUFG bank CSV.
    """
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
