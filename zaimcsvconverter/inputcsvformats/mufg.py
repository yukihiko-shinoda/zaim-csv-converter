"""This module implements row model of MUFG bank CSV."""
from __future__ import annotations

from abc import ABC
from datetime import datetime
from enum import Enum
from typing import Optional
from dataclasses import dataclass

from zaimcsvconverter.inputcsvformats import InputStoreRowData, InputRowFactory, InputRow, InputStoreRow
from zaimcsvconverter.models import AccountId
from zaimcsvconverter.utility import Utility


@dataclass
class MufgRowData(InputStoreRowData):
    """This class implements data class for wrapping list of MUFG bunk CSV row model."""
    class Summary(Enum):
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        CARD = 'カ−ド'
        CARD_CONVENIENCE_STORE_ATM = 'カ−ドＣ１'

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


class MufgRow(InputRow):
    """This class implements row model of MUFG bank CSV."""
    def __init__(self, account_id: AccountId, input_row_data: MufgRowData):
        super().__init__(account_id, input_row_data)
        self.cash_flow_kind: MufgRowData.CashFlowKind = input_row_data.cash_flow_kind
        self._summary: str = input_row_data.summary

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
        return self._summary == MufgRowData.Summary.CARD.value or \
               self._summary == MufgRowData.Summary.CARD_CONVENIENCE_STORE_ATM.value

    @property
    def is_income_from_other_own_account(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.is_income and self.is_by_card


class MufgIncomeRow(MufgRow, ABC):
    """This class implements income row model of MUFG bank CSV."""
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


class MufgPaymentRow(MufgRow, ABC):
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


class MufgIncomeFromSelfRow(MufgIncomeRow):
    """This class implements income from self row model of MUFG bank CSV."""


class MufgPaymentToSelfRow(MufgPaymentRow):
    """This class implements payment from self row model of MUFG bank CSV."""


# pylint: disable=too-many-instance-attributes
class MufgStoreRow(MufgRow, InputStoreRow, ABC):
    """This class implements row model of MUFG bank CSV."""
    @property
    def is_transfer_income_from_other_own_account(self) -> bool:
        """This method returns whether this row is transfer income from other own account or not."""
        return self.is_transfer_income and self.store.transfer_target is not None

    @property
    def is_transfer_payment_to_other_own_account(self) -> bool:
        """This method returns whether this row is transfer payment to other own account or not."""
        return self.is_transfer_payment and self.store.transfer_target is not None


# pylint: disable=too-many-ancestors
class MufgIncomeFromOthersRow(MufgStoreRow, MufgIncomeRow):
    """This class implements row model of MUFG bank CSV."""


# pylint: disable=too-many-ancestors
class MufgPaymentToSomeoneRow(MufgStoreRow, MufgPaymentRow):
    """
    This class implements payment row model of MUFG bank CSV.
    It may to others, also may to self.
    """


class MufgRowFactory(InputRowFactory[MufgRowData, MufgRow]):
    """This class implements factory to create MUFG CSV row instance."""
    def create(self, account_id: AccountId, input_row_data: MufgRowData) -> MufgRow:
        if input_row_data.is_empty_store_name and input_row_data.cash_flow_kind == MufgRowData.CashFlowKind.INCOME:
            return MufgIncomeFromSelfRow(account_id, input_row_data)
        if input_row_data.is_empty_store_name and input_row_data.cash_flow_kind == MufgRowData.CashFlowKind.PAYMENT:
            return MufgPaymentToSelfRow(account_id, input_row_data)
        if input_row_data.cash_flow_kind in (
                MufgRowData.CashFlowKind.PAYMENT, MufgRowData.CashFlowKind.TRANSFER_PAYMENT
        ):
            return MufgPaymentToSomeoneRow(account_id, input_row_data)
        if input_row_data.cash_flow_kind in (MufgRowData.CashFlowKind.INCOME, MufgRowData.CashFlowKind.TRANSFER_INCOME):
            return MufgIncomeFromOthersRow(account_id, input_row_data)
        raise ValueError(
            f'Cash flow kind is not supported. Cash flow kind = {input_row_data.cash_flow_kind}'
        )  # pragma: no cover
        # Reason: This line is insurance for future development so process must be not able to reach
