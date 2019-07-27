"""This module implements row model of MUFG bank CSV."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from dataclasses import dataclass

from zaimcsvconverter.inputcsvformats import InputStoreRowData, InputStoreRow, InputRowFactory
from zaimcsvconverter.models import AccountId
from zaimcsvconverter.utility import Utility


@dataclass
class MufgRowData(InputStoreRowData):
    """This class implements data class for wrapping list of MUFG bunk CSV row model."""
    class Summary(Enum):
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        CARD = 'カ－ド'

    class CashFlowKind(Enum):
        """This class implements constant of cash flow kind in MUFG CSV."""
        INCOME = '入金'
        PAYMENT = '支払い'
        TRANSFER_INCOME = '振替入金'
        TRANSFER_PAYMENT = '振替支払い'

    _date: str
    summary: str
    _summary_content: str
    _payed_amount: str
    _deposit_amount: str
    balance: str
    note: str
    is_uncapitalized: str
    _cash_flow_kind: str

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        return self._summary_content

    @property
    def payed_amount(self) -> Optional[int]:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return Utility.convert_string_to_int_or_none(self._payed_amount)

    @property
    def deposit_amount(self) -> Optional[int]:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return Utility.convert_string_to_int_or_none(self._deposit_amount)

    @property
    def cash_flow_kind(self) -> MufgRowData.CashFlowKind:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.CashFlowKind(self._cash_flow_kind)

    def validate(self, account_id: AccountId) -> bool:
        self.stock_error(
            lambda: self.date,
            f'Invalid date. Date = {self._date}'
        )
        self.stock_error(
            lambda: self.payed_amount,
            f'Invalid payed amount. Payed amount = {self._payed_amount}'
        )
        self.stock_error(
            lambda: self.deposit_amount,
            f'Invalid deposit amount. Deposit amount = {self._deposit_amount}'
        )
        self.stock_error(
            lambda: self.cash_flow_kind,
            'The value of "Cash flow kind" has not been defined in this code. '
            f'Cash flow kind = {self._cash_flow_kind}'
        )
        return super().validate(account_id)


# pylint: disable=too-many-instance-attributes
class MufgRow(InputStoreRow):
    """This class implements row model of MUFG bank CSV."""
    def __init__(self, account_id: AccountId, row_data: MufgRowData):
        super().__init__(account_id, row_data)
        self.cash_flow_kind: MufgRowData.CashFlowKind = row_data.cash_flow_kind
        self._summary: str = row_data.summary

    @property
    def is_income(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.cash_flow_kind == MufgRowData.CashFlowKind.INCOME

    @property
    def is_payment(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.cash_flow_kind == MufgRowData.CashFlowKind.PAYMENT

    @property
    def is_transfer_income(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.cash_flow_kind == MufgRowData.CashFlowKind.TRANSFER_INCOME

    @property
    def is_transfer_payment(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.cash_flow_kind == MufgRowData.CashFlowKind.TRANSFER_PAYMENT

    @property
    def is_by_card(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self._summary == MufgRowData.Summary.CARD.value


class MufgIncomeRow(MufgRow):
    """This class implements row model of MUFG bank CSV."""
    def __init__(self, account_id: AccountId, row_data: MufgRowData):
        super().__init__(account_id, row_data)
        self._deposit_amount: Optional[int] = row_data.deposit_amount

    @property
    def deposit_amount(self) -> int:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        if self._deposit_amount is None:
            raise ValueError('Deposit amount on income row is not allowed empty.')
        return self._deposit_amount

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.deposit_amount,
            f'Deposit amount in income row is required. Deposit amount = {self._deposit_amount}'
        )
        return super().validate


class MufgPaymentRow(MufgRow):
    """This class implements payment row model of MUFG bank CSV."""
    def __init__(self, account_id: AccountId, row_data: MufgRowData):
        super().__init__(account_id, row_data)
        self._payed_amount: Optional[int] = row_data.payed_amount

    @property
    def payed_amount(self) -> int:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        if self._payed_amount is None:
            raise ValueError('Payed amount on payment row is not allowed empty.')
        return self._payed_amount

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.payed_amount,
            f'Payed amount in payment row is required. Payed amount = {self._payed_amount}'
        )
        return super().validate


class MufgRowFactory(InputRowFactory[MufgRowData, MufgRow]):
    """This class implements factory to create MUFG CSV row instance."""
    def create(self, account_id: AccountId, input_row_data: MufgRowData) -> MufgRow:
        if input_row_data.cash_flow_kind in (
                MufgRowData.CashFlowKind.PAYMENT, MufgRowData.CashFlowKind.TRANSFER_PAYMENT
        ):
            return MufgPaymentRow(account_id, input_row_data)
        if input_row_data.cash_flow_kind in (MufgRowData.CashFlowKind.INCOME, MufgRowData.CashFlowKind.TRANSFER_INCOME):
            return MufgIncomeRow(account_id, input_row_data)
        raise ValueError(f'Cash flow kind is not supported. Cash flow kind = {input_row_data.cash_flow_kind}')
