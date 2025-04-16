"""Custom data type to convert string to optional int."""

from collections.abc import Callable
from typing import Any, Optional

import annotated_types

from zaimcsvconverter.customdatatypes.validators import (
    optional_int_validator,
    optional_number_multiple_validator,
    optional_number_size_validator,
    optional_strict_int_validator,
)


class OptionalIntegerMustBeFromStr:
    """Validator to convert string to optional int."""

    def __init__(self, string_to_int: Callable[[str], int]) -> None:
        self.string_to_int = string_to_int

    def validate(self, value: Any) -> Optional[int]:
        if not isinstance(value, str):
            msg = f"String required. Value is {value}. Type is {type(value)}."
            raise TypeError(msg)
        if not value:
            return None
        return self.string_to_int(value)


# Reason: Followed Pydantic specification.
def abstract_constringtooptionalint(  # noqa: PLR0913 pylint: disable=too-many-arguments
    *,
    strict: Optional[bool] = None,
    gt: Optional[int] = None,
    ge: Optional[int] = None,
    lt: Optional[int] = None,
    le: Optional[int] = None,
    multiple_of: Optional[int] = None,
) -> list[Any]:
    """A wrapper around `int` that allows for additional constraints."""
    return [
        optional_strict_int_validator if strict else optional_int_validator,
        optional_number_size_validator,
        optional_number_multiple_validator,
        annotated_types.Interval(gt=gt, ge=ge, lt=lt, le=le),
        annotated_types.MultipleOf(multiple_of) if multiple_of is not None else None,
    ]
