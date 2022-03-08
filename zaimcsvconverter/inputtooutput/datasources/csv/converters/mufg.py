"""Converter from MUFG CSV data to record model."""
from zaimcsvconverter.data.mufg import CashFlowKind
from zaimcsvconverter.inputtooutput.datasources.csv.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.mufg import MufgRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.mufg import (
    MufgIncomeFromOthersRow,
    MufgIncomeFromSelfRow,
    MufgPaymentToSelfRow,
    MufgPaymentToSomeoneRow,
    MufgRow,
)


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
