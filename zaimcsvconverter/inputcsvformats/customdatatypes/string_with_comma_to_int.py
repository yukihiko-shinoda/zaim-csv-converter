"""Custom data type to convert string with comma to int."""
from typing import Any, Optional, TYPE_CHECKING

# Reason: Pylint's bug. pylint: disable=no-name-in-module
from pydantic import ConstrainedInt

from zaimcsvconverter.utility import Utility

if TYPE_CHECKING:
    # Reason: Prioritize typing
    from pydantic.types import CallableGenerator  # type: ignore


class StringWithCommaToInt(ConstrainedInt):
    """Type that converts string with comma to int."""

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.integer_must_be_from_str
        yield from super().__get_validators__()

    @classmethod
    def integer_must_be_from_str(cls, value: Any) -> int:
        if not isinstance(value, str):
            raise TypeError("string required")
        return Utility.convert_string_with_comma_to_int(value)


def constringwithcommatoint(
    *,
    strict: bool = False,
    # Reason: Followed pydantic specification.
    gt: Optional[int] = None,  # pylint: disable=invalid-name
    ge: Optional[int] = None,  # pylint: disable=invalid-name
    lt: Optional[int] = None,  # pylint: disable=invalid-name
    le: Optional[int] = None,  # pylint: disable=invalid-name
    multiple_of: Optional[int] = None
) -> type[int]:
    """Creates constrained type for converting string with comma to int value."""
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("ConstrainedStringWithCommaToIntValue", (StringWithCommaToInt,), namespace)


if TYPE_CHECKING:
    StrictStringWithCommaToInt = int
else:
    StrictStringWithCommaToInt = constringwithcommatoint(strict=True)
