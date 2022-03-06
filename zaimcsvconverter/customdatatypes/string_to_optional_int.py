"""Custom data types."""
from decimal import Decimal
from typing import Any, Optional, TYPE_CHECKING, Union

# Reason: Pylint's bug.
from pydantic import ConstrainedInt  # pylint: disable=no-name-in-module
from pydantic.fields import ModelField  # pylint: disable=no-name-in-module,unused-import

# pylint: disable=no-name-in-module
from pydantic.validators import int_validator, number_multiple_validator, number_size_validator, strict_int_validator

from zaimcsvconverter.utility import Utility

Number = Union[int, float, Decimal]


if TYPE_CHECKING:
    # Reason: Prioritize typing
    from pydantic.types import CallableGenerator  # type: ignore


def optional_strict_int_validator(value: Any) -> Optional[int]:
    if value is None:
        return None
    return strict_int_validator(value)


def optional_int_validator(value: Any) -> Optional[int]:
    if value is None:
        return None
    return int_validator(value)


def optional_number_size_validator(value: Optional["Number"], field: "ModelField") -> Optional["Number"]:
    if value is None:
        return None
    return number_size_validator(value, field)


def optional_number_multiple_validator(value: Optional["Number"], field: "ModelField") -> Optional["Number"]:
    if value is None:
        return None
    return number_multiple_validator(value, field)


class StringToOptionalInt(ConstrainedInt):
    """Optional pydantic ConstrainedInt from str."""

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.optional_integer_must_be_from_str
        yield optional_strict_int_validator if cls.strict else optional_int_validator
        yield optional_number_size_validator
        yield optional_number_multiple_validator

    @classmethod
    def optional_integer_must_be_from_str(cls, value: Any) -> Optional[int]:
        if not isinstance(value, str):
            raise TypeError("string required")
        if value == "":
            return None
        return int(value)


def constringtooptionalint(
    *,
    strict: bool = False,
    # Reason: To follow pydantic constr interface.
    gt: Optional[int] = None,  # pylint: disable=invalid-name
    ge: Optional[int] = None,  # pylint: disable=invalid-name
    lt: Optional[int] = None,  # pylint: disable=invalid-name
    le: Optional[int] = None,  # pylint: disable=invalid-name
    multiple_of: Optional[int] = None
) -> type[int]:
    """Optional pydantic conint from str."""
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("ConstrainedStringToOptionalIntValue", (StringToOptionalInt,), namespace)


if TYPE_CHECKING:
    ConstrainedStringToOptionalInt = Optional[int]
else:
    ConstrainedStringToOptionalInt = constringtooptionalint()


class StringWithCommaToOptionalInt(StringToOptionalInt):
    """Optional int from str with comma."""

    @classmethod
    def optional_integer_must_be_from_str(cls, value: Any) -> Optional[int]:
        if not isinstance(value, str):
            raise TypeError("string required")
        if value == "":
            return None
        return Utility.convert_string_with_comma_to_int(value)


def constringwithcommatooptionalint(
    *,
    strict: bool = False,
    # Reason: To follow pydantic constr interface.
    gt: Optional[int] = None,  # pylint: disable=invalid-name
    ge: Optional[int] = None,  # pylint: disable=invalid-name
    lt: Optional[int] = None,  # pylint: disable=invalid-name
    le: Optional[int] = None,  # pylint: disable=invalid-name
    multiple_of: Optional[int] = None
) -> type[int]:
    """Optional pydantic conint from str with comma."""
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("ConstrainedStringWithCommaToOptionalIntValue", (StringWithCommaToOptionalInt,), namespace)


if TYPE_CHECKING:
    ConstrainedStringWithCommaToOptionalInt = Optional[int]
else:
    ConstrainedStringWithCommaToOptionalInt = constringwithcommatooptionalint()
