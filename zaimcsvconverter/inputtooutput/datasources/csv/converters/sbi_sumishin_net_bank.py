"""Converter from SBI Sumishin net bank CSV data to record model."""
from zaimcsvconverter.inputtooutput.datasources.csv.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.sbi_sumishin_net_bank import SBISumishinNetBankRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.sbi_sumishin_net_bank import (
    SBISumishinNetBankDepositRow,
    SBISumishinNetBankRow,
    SBISumishinNetBankWithdrawalRow,
)


class SBISumishinNetBankRowFactory(InputRowFactory[SBISumishinNetBankRowData, SBISumishinNetBankRow]):
    """This class implements factory to create SBI Sumishin net bank CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: SBISumishinNetBankRowData) -> SBISumishinNetBankRow:  # type: ignore
        if input_row_data.deposit_amount is None and input_row_data.withdrawal_amount is not None:
            return SBISumishinNetBankWithdrawalRow(input_row_data)
        if input_row_data.deposit_amount is not None and input_row_data.withdrawal_amount is None:
            return SBISumishinNetBankDepositRow(input_row_data)
        raise ValueError(
            "Deposit amount and withdrawal amount is not supported. "
            f"{input_row_data.date=}, {input_row_data.deposit_amount=}, {input_row_data.withdrawal_amount=}"
        )  # pragma: no cover
