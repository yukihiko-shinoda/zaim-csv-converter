"""Zaim CSV Converter extended SBI Sumishin net bank CSV Data model."""

from datetime import datetime

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import sbi_sumishin_net_bank
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import InputStoreRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class SBISumishinNetBankRowData(sbi_sumishin_net_bank.SBISumishinNetBankRowData, InputStoreRowData):
    """This class implements data class for wrapping list of SF Card Viewer CSV row model."""

    @property
    def date(self) -> datetime:
        return self.date_

    @property
    def store_name(self) -> str:
        return self.content

    @property
    def is_withdrawal(self) -> bool:
        return self.deposit_amount is None and self.withdrawal_amount is not None

    @property
    def is_deposit(self) -> bool:
        return self.deposit_amount is not None and self.withdrawal_amount is None
