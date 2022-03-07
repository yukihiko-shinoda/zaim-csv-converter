"""This module implements convert steps from MUFG input row to Zaim row.

@see https://faq01.bk.mufg.jp/usr/file/attachment/main_contents_0401.pdf
"""
from abc import ABC, abstractmethod
from typing import cast, TypeVar

from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.converters.recordtozaim import (
    CsvRecordToZaimRowConverterFactory,
    ZaimIncomeRowStoreConverter,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
    ZaimTransferRowConverter,
)
from zaimcsvconverter.inputtooutput.datasources.csv.data.mufg import MufgRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.mufg import (
    MufgIncomeFromOthersRow,
    MufgIncomeFromSelfRow,
    MufgIncomeRow,
    MufgPaymentRow,
    MufgPaymentToSelfRow,
    MufgPaymentToSomeoneRow,
    MufgRow,
    MufgStoreRow,
)

TypeVarMufgRow = TypeVar("TypeVarMufgRow", bound=MufgRow)
TypeVarMufgIncomeRow = TypeVar("TypeVarMufgIncomeRow", bound=MufgIncomeRow)
TypeVarMufgPaymentRow = TypeVar("TypeVarMufgPaymentRow", bound=MufgPaymentRow)
TypeVarMufgIncomeFromSelfRow = TypeVar("TypeVarMufgIncomeFromSelfRow", bound=MufgIncomeFromSelfRow)
TypeVarMufgPaymentToSelfRow = TypeVar("TypeVarMufgPaymentToSelfRow", bound=MufgPaymentToSelfRow)


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class MufgZaimIncomeRowConverter(ZaimIncomeRowStoreConverter[MufgIncomeFromOthersRow, MufgRowData]):
    """This class implements convert steps from MUFG input row to Zaim income row."""

    @property
    def cash_flow_target(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.deposit_amount


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class MufgZaimPaymentRowConverter(ZaimPaymentRowStoreConverter[MufgPaymentToSomeoneRow, MufgRowData]):
    """This class implements convert steps from MUFG input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.payed_amount


# Reason: Pylint's Bug. @see https://github.com/PyCQA/pylint/issues/179 pylint: disable=abstract-method
class MufgZaimTransferRowConverter(ZaimTransferRowConverter[TypeVarMufgRow, MufgRowData], ABC):
    """This class implements convert steps from MUFG input row to Zaim transfer row."""


class MufgAbstractIncomeZaimTransferRowConverter(MufgZaimTransferRowConverter[TypeVarMufgIncomeRow]):
    """This class implements convert steps from MUFG income input row to Zaim transfer row."""

    @property
    @abstractmethod
    def cash_flow_source(self) -> str:
        """This property returns cash flow source."""

    @property
    def cash_flow_target(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.deposit_amount


class MufgAbstractPaymentZaimTransferRowConverter(MufgZaimTransferRowConverter[TypeVarMufgPaymentRow]):
    """This class implements convert steps from MUFG payment input row [MufgPaymentRow]to Zaim transfer row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.mufg.account_name

    @property
    @abstractmethod
    def cash_flow_target(self) -> str:
        """This property returns cash flow target."""

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.payed_amount


class MufgIncomeZaimTransferRowConverter(MufgAbstractIncomeZaimTransferRowConverter[MufgIncomeFromSelfRow]):
    """This class implements convert steps from MUFG income input row to Zaim transfer row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.mufg.transfer_account_name


class MufgPaymentZaimTransferRowConverter(MufgAbstractPaymentZaimTransferRowConverter[MufgPaymentToSelfRow]):
    """This class implements convert steps from MUFG payment input row to Zaim transfer row."""

    @property
    def cash_flow_target(self) -> str:
        return CONFIG.mufg.transfer_account_name


class MufgTransferIncomeZaimTransferRowConverter(MufgAbstractIncomeZaimTransferRowConverter[MufgIncomeFromOthersRow]):
    """This class implements convert steps from MUFG transfer income input row to Zaim transfer row."""

    @property
    def cash_flow_source(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.transfer_target


class MufgTransferPaymentZaimTransferRowConverter(
    MufgAbstractPaymentZaimTransferRowConverter[MufgPaymentToSomeoneRow]
):
    """This class implements convert steps from MUFG transfer payment input row to Zaim transfer row."""

    @property
    def cash_flow_target(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.transfer_target


class MufgZaimRowConverterFactory(CsvRecordToZaimRowConverterFactory[MufgRow, MufgRowData]):
    """This class implements select steps from MUFG input row to Zaim row converter."""

    # Reason: Maybe, there are no way to resolve.
    # The nearest issues: https://github.com/dry-python/returns/issues/708
    def create(self, input_row: Kind1[MufgRow, MufgRowData]) -> ZaimRowConverter[MufgRow, MufgRowData]:  # type: ignore
        dekinded_input_row = cast(MufgRow, input_row)
        if isinstance(input_row, MufgPaymentToSelfRow) and dekinded_input_row.is_payment:
            # Because, for now, payment row looks only for express withdrawing cash by ATM.
            # Reason: The returns can't detect correct type limited by if instance block.
            return MufgPaymentZaimTransferRowConverter(input_row)  # type: ignore
        if isinstance(input_row, MufgIncomeFromSelfRow) and dekinded_input_row.is_income_from_other_own_account:
            # Reason: The returns can't detect correct type limited by if instance block.
            return MufgIncomeZaimTransferRowConverter(input_row)  # type: ignore
        if isinstance(input_row, MufgIncomeFromOthersRow) and input_row.is_transfer_income_from_other_own_account:
            # Reason: The returns can't detect correct type limited by if instance block.
            return MufgTransferIncomeZaimTransferRowConverter(input_row)  # type: ignore
        if isinstance(input_row, MufgIncomeFromOthersRow):
            # Reason: The returns can't detect correct type limited by if instance block.
            return MufgZaimIncomeRowConverter(input_row)  # type: ignore
        if isinstance(input_row, MufgPaymentToSomeoneRow) and input_row.is_transfer_payment_to_other_own_account:
            # Reason: The returns can't detect correct type limited by if instance block.
            return MufgTransferPaymentZaimTransferRowConverter(input_row)  # type: ignore
        if isinstance(input_row, MufgPaymentToSomeoneRow):
            # Reason: The returns can't detect correct type limited by if instance block.
            return MufgZaimPaymentRowConverter(input_row)  # type: ignore
        raise ValueError(self.build_message(input_row))  # pragma: no cover
        # Reason: This line is insurance for future development so process must be not able to reach

    @staticmethod
    def build_message(input_row: Kind1[MufgRow, MufgRowData]) -> str:  # pragma: no cover
        """This method builds error message."""
        message = (
            "Unsupported row. "
            f"class = {type(input_row)}, "
            f"is_income_from_other_own_account = {input_row.is_income_from_other_own_account}"
        )
        if isinstance(input_row, MufgStoreRow):
            message = f"{message}, store.transfer_target = {input_row.store.transfer_target}"
        return message
