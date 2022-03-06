"""GOLD POINT CARD+ CSV Data model version 201912."""
from pydantic.dataclasses import dataclass

from zaimcsvconverter.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.first_form_normalizer import CsvRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class GoldPointCardPlus201912RowData(CsvRowData):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV version 201912 row model."""

    used_date: StringToDateTime
    used_store: str
    used_amount: str
    number_of_division: str
    current_time_of_division: str
    payed_amount: int
    others: str
