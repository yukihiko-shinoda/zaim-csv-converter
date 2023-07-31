"""Custom data type to convert string with comma to optional int."""
from typing import Any, Optional, TYPE_CHECKING

# Reason: Pylint's bug. pylint: disable=no-name-in-module
from zaimcsvconverter.customdatatypes.string_to_optional_int import StringToOptionalInt
from zaimcsvconverter.utility import Utility


class StringWithCommaToOptionalInt(StringToOptionalInt):
    """Type that converts string with comma to optional int."""

    @classmethod
    def optional_integer_must_be_from_str(cls, value: Any) -> Optional[int]:
        if not isinstance(value, str):
            msg = "string required"
            raise TypeError(msg)
        if not value:
            return None
        return Utility.convert_string_with_comma_to_int(value)


# Reason: Followed pydantic specification.
def constringwithcommatooptionalint(  # noqa: PLR0913
    *,
    strict: bool = False,
    gt: Optional[int] = None,  # pylint: disable=invalid-name
    ge: Optional[int] = None,  # pylint: disable=invalid-name
    lt: Optional[int] = None,  # pylint: disable=invalid-name
    le: Optional[int] = None,  # pylint: disable=invalid-name
    multiple_of: Optional[int] = None,
) -> type[int]:
    """Creates constrained type for converting string with comma to int value."""
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = {"strict": strict, "gt": gt, "ge": ge, "lt": lt, "le": le, "multiple_of": multiple_of}
    return type("ConstrainedStringWithCommaToIntValue", (StringWithCommaToOptionalInt,), namespace)


# Reason: The mypy's bug:
#   error: Unsupported left operand type for == (ConstrainedStringToOptionalInt?)  [operator]
if TYPE_CHECKING:  # noqa: SIM108
    StrictStringWithCommaToOptionalInt = Optional[int]
else:
    StrictStringWithCommaToOptionalInt = constringwithcommatooptionalint(strict=True)
