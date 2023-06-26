"""This module implements row model of MUFG bank CSV."""
from __future__ import annotations

from abc import ABC
from typing import Any

from zaimcsvconverter.data.mufg import CashFlowKind
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csv.data.mufg import MufgRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputRow, InputStoreRow


class MufgRow(InputRow[MufgRowData]):
    """This class implements row model of MUFG bank CSV."""

    def __init__(self, input_row_data: MufgRowData, *args: Any, **kwargs: Any) -> None:
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

    def __init__(self, row_data: MufgRowData, *args: Any, **kwargs: Any) -> None:
        super().__init__(row_data, *args, **kwargs)
        self._deposit_amount: int | None = row_data.deposit_amount

    @property
    def deposit_amount(self) -> int:
        if self._deposit_amount is None:
            msg = "Deposit amount on income row is not allowed empty."
            raise ValueError(msg)
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
        self._payed_amount: int | None = row_data.payed_amount

    @property
    def payed_amount(self) -> int:
        if self._payed_amount is None:
            msg = "Payed amount on payment row is not allowed empty."
            raise ValueError(msg)
        return self._payed_amount

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.payed_amount,
            f"Payed amount in payment row is required. Payed amount = {self._payed_amount}",
        )
        return super().validate


class MufgIncomeFromSelfRow(MufgIncomeRow):
    """This class implements income from self row model of MUFG bank CSV."""


class MufgPaymentToSelfRow(MufgPaymentRow):
    """This class implements payment from self row model of MUFG bank CSV."""


# pylint: disable=too-many-instance-attributes
class MufgStoreRow(MufgRow, InputStoreRow[MufgRowData], ABC):
    """This class implements row model of MUFG bank CSV."""

    def __init__(self, input_row_data: MufgRowData) -> None:
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
