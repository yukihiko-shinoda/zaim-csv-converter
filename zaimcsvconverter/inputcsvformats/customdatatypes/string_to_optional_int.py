"""Custom data types."""
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


class StringWithCommaToOptionalInt(StringToOptionalInt):
    @classmethod
    def optional_integer_must_be_from_str(cls, v: Any) -> Optional[int]:
        if not isinstance(v, str):
            raise TypeError("string required")
        if v == "":
            return None
        return Utility.convert_string_with_comma_to_int(v)


def constringwithcommatooptionalint(
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
    return type("ConstrainedStringWithCommaToOptionalIntValue", (StringWithCommaToOptionalInt,), namespace)


if TYPE_CHECKING:
    ConstrainedStringWithCommaToOptionalInt = Optional[int]
else:
    ConstrainedStringWithCommaToOptionalInt = constringwithcommatooptionalint()
