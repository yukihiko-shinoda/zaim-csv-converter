"""SBI Sumishin net bank CSV Data model."""

from pydantic.dataclasses import dataclass

from zaimcsvconverter.customdatatypes.string_to_datetime import StringSlashToDateTime
from zaimcsvconverter.customdatatypes.string_with_comma_to_optional_int import StrictStringWithCommaToOptionalInt
from zaimcsvconverter.first_form_normalizer import CsvRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class SBISumishinNetBankRowData(CsvRowData):
    """This class implements data class for wrapping list of SF Card Viewer CSV row model."""

    date_: StringSlashToDateTime
    content: str
    withdrawal_amount: StrictStringWithCommaToOptionalInt
    deposit_amount: StrictStringWithCommaToOptionalInt
    balance: str
    note: str
