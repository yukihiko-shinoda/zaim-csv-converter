"""Custom data type to convert yen string to int."""
from typing import TYPE_CHECKING

# Reason: Pylint's bug. pylint: disable=no-name-in-module
from zaimcsvconverter.customdatatypes.abstract_string_to_int import ConstrainedStringToInt, constringtoint
from zaimcsvconverter.utility import Utility


class KanjiYenStringToInt(ConstrainedStringToInt):
    """Type that converts string with comma to int."""

    @classmethod
    def string_to_int(cls, value: str) -> int:
        return Utility.convert_kanji_yen_string_to_int(value)


if TYPE_CHECKING:
    StrictKanjiYenStringToInt = int
else:
    StrictKanjiYenStringToInt = constringtoint("ConstrainedKanjiYenStringToIntValue", KanjiYenStringToInt, strict=True)
