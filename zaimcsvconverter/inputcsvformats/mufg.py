"""This module implements row model of MUFG bank CSV."""

from datetime import datetime
from enum import Enum
from typing import Optional
from dataclasses import dataclass

from zaimcsvconverter.exceptions import InvalidRowError
from zaimcsvconverter.inputcsvformats import InputStoreRowData, InputStoreRow, InputRowFactory, ValidatedInputStoreRow
from zaimcsvconverter.models import AccountId
from zaimcsvconverter.utility import Utility


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
    """This class implements row model of MUFG bank CSV."""
    class CashFlowKind(Enum):
        """This class implements constant of cash flow kind in MUFG CSV."""
        INCOME = '入金'
        PAYMENT = '支払い'
        TRANSFER_INCOME = '振替入金'
        TRANSFER_PAYMENT = '振替支払い'

    def __init__(self, account_id: AccountId, row_data: MufgRowData):
        super().__init__(account_id, row_data)
        self._summary: str = row_data.summary
        self.payed_amount: Optional[int] = Utility.convert_string_to_int_or_none(row_data.payed_amount)
        self.deposit_amount: Optional[int] = Utility.convert_string_to_int_or_none(row_data.deposit_amount)
        self.cash_flow_kind: Optional[MufgRow.CashFlowKind] = MufgRow.CashFlowKind(row_data.cash_flow_kind)

    def validate(self) -> ValidatedInputStoreRow:
        if self.cash_flow_kind is None:
            raise InvalidRowError(
                'The value of "Cash flow kind" has not been defined in this code.'
                f'Cash flow kind = {self.data.cash_flow_kind}'
            )
        return super().validate()

    @property
    def is_by_card(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self._summary == 'カ－ド'

    @property
    def is_income(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.cash_flow_kind == MufgRow.CashFlowKind.INCOME

    @property
    def is_payment(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.cash_flow_kind == MufgRow.CashFlowKind.PAYMENT

    @property
    def is_transfer_income(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.cash_flow_kind == MufgRow.CashFlowKind.TRANSFER_INCOME

    @property
    def is_transfer_payment(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.cash_flow_kind == MufgRow.CashFlowKind.TRANSFER_PAYMENT


class MufgRowFactory(InputRowFactory):
    """This class implements factory to create MUFG CSV row instance."""
    def create(self, account_id: AccountId, row_data: MufgRowData) -> MufgRow:
        return MufgRow(account_id, row_data)
