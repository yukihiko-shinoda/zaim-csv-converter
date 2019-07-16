"""This module implements row model of MUFG bank CSV."""

from __future__ import annotations
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional, Dict, Type
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.input_row import InputStoreRowData, InputRowFactory, InputStoreRow
from zaimcsvconverter.models import Store
from zaimcsvconverter.utility import Utility
from zaimcsvconverter.zaim_row import ZaimTransferRow, ZaimIncomeRow, ZaimPaymentRow, ZaimRow

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


class MufgRowFactory(InputRowFactory):
    """This class implements factory to create MUFG CSV row instance."""
    def create(self, account: 'Account', row_data: MufgRowData) -> MufgRow:
        try:
            cash_flow_kind = CashFlowKind(row_data.cash_flow_kind)
        except ValueError as error:
            raise ValueError(
                'The value of "Cash flow kind" has not been defined in this code.'
                f'Cash flow kind = {row_data.cash_flow_kind}'
            ) from error

        mufg_row_class = self.get_appropriate_row_class(cash_flow_kind)
        return mufg_row_class(account, row_data)

    @staticmethod
    def get_appropriate_row_class(cash_flow_kind: CashFlowKind) -> Type[MufgRow]:
        """This method returns appropriate row class."""
        dictionary_mufg_row: Dict[CashFlowKind, Type[MufgRow]] = {
            CashFlowKind.INCOME: MufgIncomeRow,
            CashFlowKind.PAYMENT: MufgPaymentRow,
            CashFlowKind.TRANSFER_INCOME: MufgTransferIncomeRow,
            CashFlowKind.TRANSFER_PAYMENT: MufgTransferPaymentRow,
        }
        mufg_row_class = dictionary_mufg_row.get(cash_flow_kind)
        if mufg_row_class is None:
            raise ValueError(f'The mufg_row_class for {cash_flow_kind} has not been defined in this code.')
        return mufg_row_class


@dataclass
class MufgRowData(InputStoreRowData):
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
        return datetime.strptime(self._date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        return self._summary_content


# pylint: disable=too-many-instance-attributes
class MufgRow(InputStoreRow):
    """
    This class implements row model of MUFG bank CSV.
    """
    def __init__(self, account: 'Account', row_data: MufgRowData):
        super().__init__(account, row_data)
        self._summary: str = row_data.summary
        self._payed_amount: Optional[int] = Utility.convert_string_to_int_or_none(row_data.payed_amount)
        self._deposit_amount: Optional[int] = Utility.convert_string_to_int_or_none(row_data.deposit_amount)

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
    def _amount(self) -> Optional[int]:
        pass

    @property
    def zaim_income_cash_flow_target(self) -> str:
        return self._cash_flow_target_on_zaim

    @property
    def zaim_income_ammount_income(self) -> int:
        if self._amount is None:
            raise ValueError('Income amount on MUFG income row must be not None.')
        return self._amount

    @property
    def zaim_payment_cash_flow_source(self) -> str:
        return self._cash_flow_source_on_zaim

    @property
    def zaim_payment_amount_payment(self) -> int:
        if self._amount is None:
            raise ValueError('Payment amount on MUFG payment row must be not None.')
        return self._amount

    @property
    def zaim_transfer_cash_flow_source(self) -> str:
        return self._cash_flow_source_on_zaim

    @property
    def zaim_transfer_cash_flow_target(self) -> str:
        return self._cash_flow_target_on_zaim

    @property
    def zaim_transfer_amount_transfer(self) -> int:
        if self._amount is None:
            raise ValueError('Transfer amount on MUFG transfer row must be not None.')
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
        if self._deposit_amount is None:
            raise ValueError('Deposit amount on income row must be not None.')
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
    def _amount(self) -> Optional[int]:
        return self._payed_amount


class MufgIncomeRow(MufgAbstractIncomeRow):
    """
    This class implements income row model of MUFG bank CSV.
    """
    def zaim_row_class_to_convert(self, store: Store) -> Type['ZaimRow']:
        if self._summary == 'カ－ド':
            return ZaimTransferRow
        return ZaimIncomeRow

    @property
    def _cash_flow_source_on_zaim(self) -> str:
        return CONFIG.mufg.transfer_account_name


class MufgPaymentRow(MufgAbstractPaymentRow):
    """
    This class implements payment row model of MUFG bank CSV.
    """
    def zaim_row_class_to_convert(self, store: Store) -> Type['ZaimTransferRow']:
        return ZaimTransferRow

    @property
    def _cash_flow_target_on_zaim(self) -> str:
        return CONFIG.mufg.transfer_account_name


class MufgTransferIncomeRow(MufgAbstractIncomeRow):
    """
    This class implements transfer income row model of MUFG bank CSV.
    """
    def zaim_row_class_to_convert(self, store: Store) -> Type['ZaimRow']:
        if store.transfer_target is None:
            return ZaimIncomeRow
        return ZaimTransferRow

    @property
    def _cash_flow_source_on_zaim(self) -> str:
        if self.zaim_store is None:
            raise UnboundLocalError('Store data on this row is not in database.')
        return self.zaim_store.transfer_target


class MufgTransferPaymentRow(MufgAbstractPaymentRow):
    """
    This class implements transfer payment row model of MUFG bank CSV.
    """
    def zaim_row_class_to_convert(self, store: Store) -> Type['ZaimRow']:
        if store.transfer_target is None:
            return ZaimPaymentRow
        return ZaimTransferRow

    @property
    def _cash_flow_target_on_zaim(self) -> str:
        if self.zaim_store is None:
            raise UnboundLocalError('Store data on this row is not in database.')
        return self.zaim_store.transfer_target
