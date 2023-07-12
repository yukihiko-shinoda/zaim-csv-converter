"""Mobile Suica CSV Data model."""
from enum import Enum

from pydantic.dataclasses import dataclass

from zaimcsvconverter.customdatatypes.string_to_datetime import StringSlashMonthDayOnlyToDatetime
from zaimcsvconverter.customdatatypes.string_with_comma_to_optional_int import StrictStringWithCommaToOptionalInt
from zaimcsvconverter.customdatatypes.symbol_yen_string_to_int import StrictSymbolYenStringToInt
from zaimcsvconverter.first_form_normalizer import CsvRowData


# Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
class Kind1(str, Enum):
    """This class implements constant of kind 1 in Mobile Suica CSV."""

    SALES_GOODS = "物販"
    ENTER = "入"
    # Reason: Specification.
    LAYOVER = "＊入"  # noqa: RUF001
    AUTO_CHARGE = "ｵｰﾄ"
    BUS_ETC = "ﾊﾞｽ等"
    VIEW = "VIEW"
    CARD = "ｶｰﾄﾞ"
    # Includes JRE point
    CASH = "現金"
    EXCHANGE_OTHER_TICKET = "購"
    # Reason: This is not password.
    COMMUTER_PASS = "定"  # nosec  # noqa: S105


class Kind2(str, Enum):
    """This class implements constant of kind 1 in Mobile Suica CSV."""

    EMPTY = ""
    EXIT = "出"
    EXIT_BY_WINDOW = "精"
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
    # Reason: Now we don't have enough time to recreate type class:
    # - Answer: python - How can mypy accept pydantic's constr() types? - Stack Overflow
    #   https://stackoverflow.com/a/67871116/12721873
    deposit_used_amount: StrictStringWithCommaToOptionalInt  # type: ignore[valid-type]
