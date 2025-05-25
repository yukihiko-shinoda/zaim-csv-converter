"""Validators."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import Union

# pylint: disable=no-name-in-module
from pydantic.v1.validators import int_validator
from pydantic.v1.validators import number_multiple_validator
from pydantic.v1.validators import number_size_validator
from pydantic.v1.validators import strict_int_validator

if TYPE_CHECKING:
    from pydantic.v1.fields import ModelField  # pylint: disable=no-name-in-module,unused-import


Number = Union[int, float, Decimal]


def optional_strict_int_validator(value: Any) -> Optional[int]:
    if value is None:
        return None
    return strict_int_validator(value)


def optional_int_validator(value: Any) -> Optional[int]:
    if value is None:
        return None
    return int_validator(value)


def optional_number_size_validator(value: Optional[Number], field: ModelField) -> Optional[Number]:
    if value is None:
        return None
    return number_size_validator(value, field)


def optional_number_multiple_validator(value: Optional[Number], field: ModelField) -> Optional[Number]:
    if value is None:
        return None
    return number_multiple_validator(value, field)


def string_validator(value: Any) -> str:
    if not isinstance(value, str):
        msg = "string required"
        raise TypeError(msg)
    return value
