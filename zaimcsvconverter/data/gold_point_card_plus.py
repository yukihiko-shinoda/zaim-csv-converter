"""GOLD POINT CARD+ CSV Data model."""

from pydantic.dataclasses import dataclass

from zaimcsvconverter.customdatatypes.string_to_datetime import StringSlashToDateTime
from zaimcsvconverter.first_form_normalizer import CsvRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods,too-many-instance-attributes
class GoldPointCardPlusRowData(CsvRowData):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV row model."""

    used_date: StringSlashToDateTime
    used_store: str
    used_card: str
    payment_kind: str
    number_of_division: str
    scheduled_payment_month: str
    used_amount: int
    unknown_1: str
    unknown_2: str
    unknown_3: str
    unknown_4: str
    unknown_5: str
    unknown_6: str
