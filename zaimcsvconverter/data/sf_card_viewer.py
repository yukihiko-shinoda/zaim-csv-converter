"""SF Card Viewer CSV Data model."""
from enum import Enum

from pydantic.dataclasses import dataclass

from zaimcsvconverter.customdatatypes.string_to_datetime import StringSlashToDateTime
from zaimcsvconverter.first_form_normalizer import CsvRowData


# Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
class Note(str, Enum):
    """This class implements constant of note in SF Card Viewer CSV."""

    EMPTY = ""
    SALES_GOODS = "物販"
    AUTO_CHARGE = "ｵｰﾄﾁｬｰｼﾞ"
    EXIT_BY_WINDOW = "窓出"
    BUS_TRAM = "ﾊﾞｽ/路面等"


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class SFCardViewerRowData(CsvRowData):
    """This class implements data class for wrapping list of SF Card Viewer CSV row model."""

    used_date: StringSlashToDateTime
    is_commuter_pass_enter: str
    railway_company_name_enter: str
    station_name_enter: str
    is_commuter_pass_exit: str
    railway_company_name_exit: str
    station_name_exit: str
    used_amount: int
    balance: str
    note: Note
