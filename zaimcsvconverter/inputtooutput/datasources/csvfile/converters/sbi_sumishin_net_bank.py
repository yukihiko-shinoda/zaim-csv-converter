"""Converter from SBI Sumishin net bank CSV data to record model."""

from zaimcsvconverter.inputtooutput.datasources.csvfile.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.sbi_sumishin_net_bank import SBISumishinNetBankRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.sbi_sumishin_net_bank import (
    SBISumishinNetBankDepositRow,  # noqa: H301
)
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.sbi_sumishin_net_bank import SBISumishinNetBankRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.sbi_sumishin_net_bank import (
    SBISumishinNetBankWithdrawalRow,  # noqa: H301
)


class SBISumishinNetBankRowFactory(InputRowFactory[SBISumishinNetBankRowData, SBISumishinNetBankRow]):
    """This class implements factory to create SBI Sumishin net bank CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: SBISumishinNetBankRowData) -> SBISumishinNetBankRow:  # type: ignore[override]
        if input_row_data.is_withdrawal:
            return SBISumishinNetBankWithdrawalRow(input_row_data)
        if input_row_data.is_deposit:
            return SBISumishinNetBankDepositRow(input_row_data)
        msg = (  # pragma: no cover
            "Deposit amount and withdrawal amount is not supported. "
            f"input_row_data.date={input_row_data.date!r}, "
            f"input_row_data.deposit_amount={input_row_data.deposit_amount!r}, "
            f"input_row_data.withdrawal_amount={input_row_data.withdrawal_amount!r}"
        )
        raise ValueError(msg)  # pragma: no cover
