"""Custom data types."""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated
from typing import Optional
from typing import Union

from pydantic import BeforeValidator

from zaimcsvconverter.customdatatypes.abstract_string_to_optional_int import OptionalIntegerMustBeFromStr
from zaimcsvconverter.customdatatypes.abstract_string_to_optional_int import abstract_constringtooptionalint
from zaimcsvconverter.customdatatypes.validators import optional_int_validator
from zaimcsvconverter.customdatatypes.validators import optional_number_multiple_validator
from zaimcsvconverter.customdatatypes.validators import optional_number_size_validator

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

Number = Union[int, float, Decimal]


# Reason: Followed Pydantic specification.
def constringtooptionalint(  # noqa: PLR0913 pylint: disable=too-many-arguments
    *,
    strict: bool | None = None,
    gt: int | None = None,
    ge: int | None = None,
    lt: int | None = None,
    le: int | None = None,
    multiple_of: int | None = None,
) -> type[int | None]:
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
        BeforeValidator(OptionalIntegerMustBeFromStr(int).validate),
        Unpack[abstract_constringtooptionalint(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)],
    ]


ConstrainedStringToOptionalInt = Annotated[
    Optional[int],
    BeforeValidator(OptionalIntegerMustBeFromStr(int).validate),
    optional_int_validator,
    optional_number_size_validator,
    optional_number_multiple_validator,
]
