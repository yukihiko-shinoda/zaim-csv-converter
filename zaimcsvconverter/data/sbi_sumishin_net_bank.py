"""SBI Sumishin net bank CSV Data model."""
from pydantic.dataclasses import dataclass

from zaimcsvconverter.first_form_normalizer import CsvRowData
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_optional_int import (
    ConstrainedStringWithCommaToOptionalInt,
)


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class SBISumishinNetBankRowData(CsvRowData):
    """This class implements data class for wrapping list of SF Card Viewer CSV row model."""

    date_: StringToDateTime
    content: str
    withdrawal_amount: ConstrainedStringWithCommaToOptionalInt
    deposit_amount: ConstrainedStringWithCommaToOptionalInt
    balance: str
    note: str
