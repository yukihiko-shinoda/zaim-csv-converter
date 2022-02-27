"""Custom data types."""
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional, TYPE_CHECKING, Union

# Reason: Pylint's bug.
from pydantic import ConstrainedInt  # pylint: disable=no-name-in-module
from pydantic.fields import ModelField
from pydantic.validators import int_validator, number_multiple_validator, number_size_validator, strict_int_validator

from zaimcsvconverter.utility import Utility

Number = Union[int, float, Decimal]


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


def optional_strict_int_validator(v: Any) -> Optional[int]:
    if v is None:
        return None
    return strict_int_validator(v)


def optional_int_validator(v: Any) -> Optional[int]:
    if v is None:
        return None
    return int_validator(v)


def optional_number_size_validator(v: Optional["Number"], field: "ModelField") -> Optional["Number"]:
    if v is None:
        return None
    return number_size_validator(v, field)


def optional_number_multiple_validator(v: Optional["Number"], field: "ModelField") -> Optional["Number"]:
    if v is None:
        return None
    return number_multiple_validator(v, field)


class StringToOptionalInt(ConstrainedInt):
    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.optional_integer_must_be_from_str
        yield optional_strict_int_validator if cls.strict else optional_int_validator
        yield optional_number_size_validator
        yield optional_number_multiple_validator

    @classmethod
    def optional_integer_must_be_from_str(cls, v: Any) -> Optional[int]:
        if not isinstance(v, str):
            raise TypeError("string required")
        if v == "":
            return None
        return int(v)


def constringtooptionalint(
    *,
    strict: bool = False,
    gt: Optional[int] = None,
    ge: Optional[int] = None,
    lt: Optional[int] = None,
    le: Optional[int] = None,
    multiple_of: Optional[int] = None
) -> type[int]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("ConstrainedStringToOptionalIntValue", (StringToOptionalInt,), namespace)


if TYPE_CHECKING:
    ConstrainedStringToOptionalInt = Optional[int]
else:
    ConstrainedStringToOptionalInt = constringtooptionalint()
