"""Custom data type to convert string with comma to optional int."""

from typing import Annotated
from typing import Optional

from pydantic import BeforeValidator

from zaimcsvconverter.customdatatypes.abstract_string_to_optional_int import OptionalIntegerMustBeFromStr
from zaimcsvconverter.customdatatypes.abstract_string_to_optional_int import abstract_constringtooptionalint
from zaimcsvconverter.customdatatypes.validators import optional_number_multiple_validator
from zaimcsvconverter.customdatatypes.validators import optional_number_size_validator
from zaimcsvconverter.customdatatypes.validators import optional_strict_int_validator
from zaimcsvconverter.utility import Utility

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


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
        BeforeValidator(OptionalIntegerMustBeFromStr(Utility.convert_string_with_comma_to_int).validate),
        Unpack[abstract_constringtooptionalint(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)],
    ]


StrictStringWithCommaToOptionalInt = Annotated[
    Optional[int],
    BeforeValidator(OptionalIntegerMustBeFromStr(Utility.convert_string_with_comma_to_int).validate),
    optional_strict_int_validator,
    optional_number_size_validator,
    optional_number_multiple_validator,
]
