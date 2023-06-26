"""Custom data type to convert yen string to int."""
from typing import TYPE_CHECKING

# Reason: Pylint's bug. pylint: disable=no-name-in-module
from zaimcsvconverter.customdatatypes.abstract_string_to_int import ConstrainedStringToInt, constringtoint
from zaimcsvconverter.utility import Utility


class SymbolYenStringToInt(ConstrainedStringToInt):
    """Type that converts string with comma to int."""

    @classmethod
    def string_to_int(cls, value: str) -> int:
        return Utility.convert_symbol_yen_string_to_int(value)


if TYPE_CHECKING:
    StrictSymbolYenStringToInt = int
else:
    StrictSymbolYenStringToInt = constringtoint(
        "ConstrainedSymbolYenStringToIntValue",
        SymbolYenStringToInt,
        strict=True,
    )
