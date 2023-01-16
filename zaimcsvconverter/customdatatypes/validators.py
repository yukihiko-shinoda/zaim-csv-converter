"""Validators."""
from decimal import Decimal
from typing import Any, Optional, Union

from pydantic.fields import ModelField  # pylint: disable=no-name-in-module,unused-import

# pylint: disable=no-name-in-module
from pydantic.validators import int_validator, number_multiple_validator, number_size_validator, strict_int_validator

Number = Union[int, float, Decimal]


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
