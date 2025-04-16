"""Custom data types."""

from decimal import Decimal
from typing import Annotated, Any, Optional, Union

import annotated_types
from pydantic import BeforeValidator

from zaimcsvconverter.customdatatypes.validators import (
    optional_int_validator,
    optional_number_multiple_validator,
    optional_number_size_validator,
    optional_strict_int_validator,
)

Number = Union[int, float, Decimal]


def optional_integer_must_be_from_str(value: Any) -> Optional[int]:
    """Optional integer must be from str."""
    if not isinstance(value, str):
        msg = "string required"
        raise TypeError(msg)
    if not value:
        return None
    return int(value)


# Reason: Followed Pydantic specification.
def constringtooptionalint(  # noqa: PLR0913 pylint: disable=too-many-arguments
    *,
    strict: bool | None = None,
    gt: int | None = None,
    ge: int | None = None,
    lt: int | None = None,
    le: int | None = None,
    multiple_of: int | None = None,
) -> type[Optional[int]]:
    """A wrapper around `int` that allows for additional constraints.

    Args:
        strict: Whether to validate the integer in strict mode. Defaults to `None`.
        gt: The value must be greater than this.
        ge: The value must be greater than or equal to this.
        lt: The value must be less than this.
        le: The value must be less than or equal to this.
        multiple_of: The value must be a multiple of this.

    Returns:
        The wrapped integer type.
    """
    return Annotated[  # type: ignore[return-value]
        Optional[int],
        BeforeValidator(optional_integer_must_be_from_str),
        optional_strict_int_validator if strict else optional_int_validator,
        optional_number_size_validator,
        optional_number_multiple_validator,
        annotated_types.Interval(gt=gt, ge=ge, lt=lt, le=le),
        annotated_types.MultipleOf(multiple_of) if multiple_of is not None else None,
    ]


ConstrainedStringToOptionalInt = Annotated[
    Optional[int],
    BeforeValidator(optional_integer_must_be_from_str),
    optional_int_validator,
    optional_number_size_validator,
    optional_number_multiple_validator,
]
