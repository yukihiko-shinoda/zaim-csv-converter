"""VIEW CARD CSV Data model."""
from pydantic.dataclasses import dataclass

from zaimcsvconverter.first_form_normalizer import CsvRowData
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.inputcsvformats.customdatatypes.string_with_comma_to_int import StrictStringWithCommaToInt


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class ViewCardRowData(CsvRowData):
    """This class implements data class for wrapping list of VIEW CARD CSV row model."""

    used_date: StringToDateTime
    used_place: str
    used_amount: str
    refund_amount: str
    billing_amount: str
    number_of_division: str
    current_time_of_division: str
    billing_amount_current_time: StrictStringWithCommaToInt
    local_currency_amount: str
    currency_abbreviation: str
    exchange_rate: str
