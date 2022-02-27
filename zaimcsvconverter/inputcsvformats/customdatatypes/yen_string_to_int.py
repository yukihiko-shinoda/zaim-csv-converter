"""Custom data type to convert yen string to int."""
from typing import Any, Optional, TYPE_CHECKING

from pydantic import ConstrainedInt

from zaimcsvconverter.utility import Utility

if TYPE_CHECKING:
    # Reason: Prioritize typing
    from pydantic.types import CallableGenerator  # type: ignore


class YenStringToInt(ConstrainedInt):
    """Type that converts yen string to int."""

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.integer_must_be_from_str
        yield from super().__get_validators__()

    @classmethod
    def integer_must_be_from_str(cls, value: Any) -> int:
        if not isinstance(value, str):
            raise TypeError("string required")
        return Utility.convert_yen_string_to_int(value)


def conyenstringtoint(
    *,
    strict: bool = False,
    # Reason: Followed pydantic specification.
    gt: Optional[int] = None,  # pylint: disable=invalid-name
    ge: Optional[int] = None,  # pylint: disable=invalid-name
    lt: Optional[int] = None,  # pylint: disable=invalid-name
    le: Optional[int] = None,  # pylint: disable=invalid-name
    multiple_of: Optional[int] = None
) -> type[int]:
    """Creates constrained type for converting yen string to int value."""
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("ConstrainedYenStringToIntValue", (YenStringToInt,), namespace)


if TYPE_CHECKING:
    StrictYenStringToInt = int
else:
    StrictYenStringToInt = conyenstringtoint(strict=True)
