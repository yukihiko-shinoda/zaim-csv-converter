"""Custom data types."""
from datetime import datetime
from typing import Any, Optional, TYPE_CHECKING

# Reason: Pylint's bug.
from pydantic import ConstrainedInt  # pylint: disable=no-name-in-module

from zaimcsvconverter.utility import Utility

if TYPE_CHECKING:
    # Reason: Prioritize typing
    from pydantic.types import CallableGenerator  # type: ignore


class StringToDateTime(datetime):
    """Type that converts string to datetime."""

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.parse_date

    @classmethod
    def parse_date(cls, value: Any) -> datetime:
        if not isinstance(value, str):
            raise TypeError("string required")
        return datetime.strptime(value, "%Y/%m/%d")


class YenStringToInt(ConstrainedInt):
    """Type that converts yen string to int."""

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.integer_must_be_from_str
        yield from super().__get_validators__()

    @classmethod
    def integer_must_be_from_str(cls, value: Any) -> int:
        if not isinstance(value, str):
            raise TypeError("string required")
        return Utility.convert_yen_string_to_int(value)


def conyenstringtoint(
    *,
    strict: bool = False,
    # Reason: Followed pydantic specification.
    gt: Optional[int] = None,  # pylint: disable=invalid-name
    ge: Optional[int] = None,  # pylint: disable=invalid-name
    lt: Optional[int] = None,  # pylint: disable=invalid-name
    le: Optional[int] = None,  # pylint: disable=invalid-name
    multiple_of: Optional[int] = None
) -> type[int]:
    """Creates constrained type for converting yen string to int value."""
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("ConstrainedYenStringToIntValue", (YenStringToInt,), namespace)


if TYPE_CHECKING:
    StrictYenStringToInt = int
else:
    StrictYenStringToInt = conyenstringtoint(strict=True)
