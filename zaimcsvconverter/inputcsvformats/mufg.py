"""This module implements row model of MUFG bank CSV."""
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic.dataclasses import dataclass as pydantic_dataclass

from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats import (
    AbstractPydantic,
    InputRow,
    InputRowFactory,
    InputStoreRow,
    InputStoreRowData,
)
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_optional_int import ConstrainedStringToOptionalInt


class CashFlowKind(Enum):
    """This class implements constant of cash flow kind in MUFG CSV."""

    INCOME = "入金"
    PAYMENT = "支払い"
    TRANSFER_INCOME = "振替入金"
    TRANSFER_PAYMENT = "振替支払い"


@pydantic_dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class MufgRowDataPydantic(AbstractPydantic):
    """This class implements data class for wrapping list of MUFG CSV row model."""

    date: StringToDateTime
    summary: str
    summary_content: str
    payed_amount: ConstrainedStringToOptionalInt
    deposit_amount: ConstrainedStringToOptionalInt
    balance: str
    note: str
    is_uncapitalized: str
    cash_flow_kind: CashFlowKind


@dataclass
class MufgRowData(InputStoreRowData[MufgRowDataPydantic]):
    """This class implements data class for wrapping list of MUFG bunk CSV row model."""

    # Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
    class Summary(Enum):
        CARD = "カ−ド"
        CARD_CONVENIENCE_STORE_ATM = "カ−ドＣ１"

    _date: str
    summary: str
    _summary_content: str
    _payed_amount: str
    _deposit_amount: str
    balance: str
    note: str
    is_uncapitalized: str
    _cash_flow_kind: str

    def create_pydantic(self) -> MufgRowDataPydantic:
        return MufgRowDataPydantic(
            # Reason: Maybe, there are no way to specify type before converted by pydantic
            self._date,  # type: ignore
            self.summary,
            self._summary_content,
            self._payed_amount,  # type: ignore
            self._deposit_amount,  # type: ignore
            self.balance,
            self.note,
            self.is_uncapitalized,
            self._cash_flow_kind,  # type: ignore
        )

    @property
    def date(self) -> datetime:
        return self.pydantic.date

    @property
    def store_name(self) -> str:
        return self.pydantic.summary_content

    @property
    def payed_amount(self) -> Optional[int]:
        return self.pydantic.payed_amount

    @property
    def deposit_amount(self) -> Optional[int]:
        return self.pydantic.deposit_amount

    @property
    def cash_flow_kind(self) -> CashFlowKind:
        return self.pydantic.cash_flow_kind

    @property
    def validate(self) -> bool:
        return super().validate


class MufgRow(InputRow[MufgRowData]):
    """This class implements row model of MUFG bank CSV."""

    def __init__(self, input_row_data: MufgRowData, *args: Any, **kwargs: Any):
        super().__init__(input_row_data, *args, **kwargs)
        self.cash_flow_kind: CashFlowKind = input_row_data.cash_flow_kind
        self._summary: str = input_row_data.summary

    @property
    def is_income(self) -> bool:
        return self.cash_flow_kind == CashFlowKind.INCOME

    @property
    def is_payment(self) -> bool:
        return self.cash_flow_kind == CashFlowKind.PAYMENT

    @property
    def is_transfer_income(self) -> bool:
        return self.cash_flow_kind == CashFlowKind.TRANSFER_INCOME

    @property
    def is_transfer_payment(self) -> bool:
        return self.cash_flow_kind == CashFlowKind.TRANSFER_PAYMENT

    @property
    def is_by_card(self) -> bool:
        return self._summary in (
            MufgRowData.Summary.CARD.value,
            MufgRowData.Summary.CARD_CONVENIENCE_STORE_ATM.value,
        )

    @property
    def is_income_from_other_own_account(self) -> bool:
        return self.is_income and self.is_by_card


class MufgIncomeRow(MufgRow, ABC):
    """This class implements income row model of MUFG bank CSV."""

    def __init__(self, row_data: MufgRowData, *args: Any, **kwargs: Any):
        super().__init__(row_data, *args, **kwargs)
        self._deposit_amount: Optional[int] = row_data.deposit_amount

    @property
    def deposit_amount(self) -> int:
        if self._deposit_amount is None:
            raise ValueError("Deposit amount on income row is not allowed empty.")
        return self._deposit_amount

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.deposit_amount,
            f"Deposit amount in income row is required. Deposit amount = {self._deposit_amount}",
        )
        return super().validate


class MufgPaymentRow(MufgRow, ABC):
    """This class implements payment row model of MUFG bank CSV."""

    def __init__(self, row_data: MufgRowData, *args: Any, **kwargs: Any) -> None:
        super().__init__(row_data, *args, **kwargs)
        self._payed_amount: Optional[int] = row_data.payed_amount

    @property
    def payed_amount(self) -> int:
        if self._payed_amount is None:
            raise ValueError("Payed amount on payment row is not allowed empty.")
        return self._payed_amount

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.payed_amount, f"Payed amount in payment row is required. Payed amount = {self._payed_amount}"
        )
        return super().validate


class MufgIncomeFromSelfRow(MufgIncomeRow):
    """This class implements income from self row model of MUFG bank CSV."""


class MufgPaymentToSelfRow(MufgPaymentRow):
    """This class implements payment from self row model of MUFG bank CSV."""


# pylint: disable=too-many-instance-attributes
class MufgStoreRow(MufgRow, InputStoreRow[MufgRowData], ABC):
    """This class implements row model of MUFG bank CSV."""

    def __init__(self, input_row_data: MufgRowData):
        super().__init__(input_row_data, FileCsvConvert.MUFG.value)

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
    """This class implements payment row model of MUFG bank CSV.

    It may to others, also may to self.
    """


class MufgRowFactory(InputRowFactory[MufgRowData, MufgRow]):
    """This class implements factory to create MUFG CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: MufgRowData) -> MufgRow:  # type: ignore
        if input_row_data.is_empty_store_name and input_row_data.cash_flow_kind == CashFlowKind.INCOME:
            return MufgIncomeFromSelfRow(input_row_data)
        if input_row_data.is_empty_store_name and input_row_data.cash_flow_kind == CashFlowKind.PAYMENT:
            return MufgPaymentToSelfRow(input_row_data)
        if input_row_data.cash_flow_kind in (
            CashFlowKind.PAYMENT,
            CashFlowKind.TRANSFER_PAYMENT,
        ):
            return MufgPaymentToSomeoneRow(input_row_data)
        if input_row_data.cash_flow_kind in (
            CashFlowKind.INCOME,
            CashFlowKind.TRANSFER_INCOME,
        ):
            return MufgIncomeFromOthersRow(input_row_data)
        raise ValueError(
            f"Cash flow kind is not supported. Cash flow kind = {input_row_data.cash_flow_kind}"
        )  # pragma: no cover
        # Reason: This line is insurance for future development so process must be not able to reach
