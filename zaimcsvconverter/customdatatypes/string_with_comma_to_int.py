"""Custom data type to convert string with comma to int."""
from typing import TYPE_CHECKING

from zaimcsvconverter.customdatatypes.abstract_string_to_int import ConstrainedStringToInt, constringtoint
from zaimcsvconverter.utility import Utility


class StringWithCommaToInt(ConstrainedStringToInt):
    """Type that converts string with comma to int."""

    @classmethod
    def string_to_int(cls, value: str) -> int:
        return Utility.convert_string_with_comma_to_int(value)


if TYPE_CHECKING:
    StrictStringWithCommaToInt = int
else:
    StrictStringWithCommaToInt = constringtoint(
        "ConstrainedStringWithCommaToIntValue", StringWithCommaToInt, strict=True
    )
