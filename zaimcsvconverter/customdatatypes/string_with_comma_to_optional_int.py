"""Custom data type to convert string with comma to optional int."""

from typing import Annotated, Any, Optional

import annotated_types
from pydantic import BeforeValidator

from zaimcsvconverter.customdatatypes.validators import (
    optional_int_validator,
    optional_number_multiple_validator,
    optional_number_size_validator,
    optional_strict_int_validator,
)
from zaimcsvconverter.utility import Utility


def optional_integer_must_be_from_str(value: Any) -> Optional[int]:
    if not isinstance(value, str):
        msg = "string required"
        raise TypeError(msg)
    if not value:
        return None
    return Utility.convert_string_with_comma_to_int(value)


# Reason: Followed pydantic specification.
def constringwithcommatooptionalint(  # noqa: PLR0913 pylint: disable=too-many-arguments
    *,
    strict: bool = False,
    gt: Optional[int] = None,  # pylint: disable=invalid-name
    ge: Optional[int] = None,  # pylint: disable=invalid-name
    lt: Optional[int] = None,  # pylint: disable=invalid-name
    le: Optional[int] = None,  # pylint: disable=invalid-name
    multiple_of: Optional[int] = None,
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


StrictStringWithCommaToOptionalInt = Annotated[
    Optional[int],
    BeforeValidator(optional_integer_must_be_from_str),
    optional_strict_int_validator,
    optional_number_size_validator,
    optional_number_multiple_validator,
]
