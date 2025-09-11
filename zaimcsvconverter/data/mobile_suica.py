"""Mobile Suica CSV Data model."""

from enum import Enum

from pydantic.dataclasses import dataclass
from pydantictypes.string_to_datetime import StringSlashMonthDayOnlyToDatetime
from pydantictypes.string_with_comma_to_optional_int import StrictStringWithCommaToOptionalInt
from pydantictypes.symbol_yen_string_to_int import StrictSymbolYenStringToInt

from zaimcsvconverter.first_form_normalizer import CsvRowData


# Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
class Kind1(str, Enum):
    """This class implements constant of kind 1 in Mobile Suica CSV."""

    SALES_GOODS = "物販"
    ENTER = "入"
    # Reason: Specification.
    LAYOVER = "＊入"  # noqa: RUF001
    AUTO_CHARGE = "ｵｰﾄ"
    BUS_ET_CETERA = "ﾊﾞｽ等"
    VIEW = "VIEW"
    CARD = "ｶｰﾄﾞ"
    # Includes JRE point
    CASH = "現金"
    EXCHANGE_OTHER_TICKET = "購"
    # Reason: This is not password.
    COMMUTER_PASS = "定"  # nosec  # noqa: S105
    SETTLE = "精"


class Kind2(str, Enum):
    """This class implements constant of kind 1 in Mobile Suica CSV."""

    EMPTY = ""
    EXIT = "出"
    EXIT_BY_WINDOW = "窓出"
    # Reason: This is not password.
    COMMUTER_PASS = "定"  # nosec  # noqa: S105


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class MobileSuicaRowData(CsvRowData):
    """This class implements data class for wrapping list of Mobile Suica CSV row model."""

    month_date: StringSlashMonthDayOnlyToDatetime
    kind_1: Kind1
    used_place_1: str
    kind_2: Kind2
    used_place_2: str
    balance: StrictSymbolYenStringToInt
    deposit_used_amount: StrictStringWithCommaToOptionalInt
