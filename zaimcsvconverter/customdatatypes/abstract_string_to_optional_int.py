"""Custom data type to convert string to optional int."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

import annotated_types

from zaimcsvconverter.customdatatypes.validators import optional_int_validator
from zaimcsvconverter.customdatatypes.validators import optional_number_multiple_validator
from zaimcsvconverter.customdatatypes.validators import optional_number_size_validator
from zaimcsvconverter.customdatatypes.validators import optional_strict_int_validator

if TYPE_CHECKING:
    from collections.abc import Callable


class OptionalIntegerMustBeFromStr:
    """Validator to convert string to optional int."""

    def __init__(self, string_to_int: Callable[[str], int]) -> None:
        self.string_to_int = string_to_int

    def validate(self, value: Any) -> int | None:
        if not isinstance(value, str):
            msg = f"String required. Value is {value}. Type is {type(value)}."
            raise TypeError(msg)
        if not value:
            return None
        return self.string_to_int(value)


# Reason: Followed Pydantic specification.
def abstract_constringtooptionalint(  # noqa: PLR0913 pylint: disable=too-many-arguments
    *,
    strict: bool | None = None,
    gt: int | None = None,
    ge: int | None = None,
    lt: int | None = None,
    le: int | None = None,
    multiple_of: int | None = None,
) -> list[Any]:
    """A wrapper around `int` that allows for additional constraints."""
    return [
        optional_strict_int_validator if strict else optional_int_validator,
        optional_number_size_validator,
        optional_number_multiple_validator,
        annotated_types.Interval(gt=gt, ge=ge, lt=lt, le=le),
        annotated_types.MultipleOf(multiple_of) if multiple_of is not None else None,
    ]
