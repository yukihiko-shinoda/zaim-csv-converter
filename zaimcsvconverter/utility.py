"""This module implements utility."""

from __future__ import annotations

import re


class Utility:
    """This class implements utility."""

    @staticmethod
    def convert_string_to_int_or_none(string: str) -> int | None:
        """This method converts string to int or None."""
        if not string:
            return None
        return int(string.replace(",", ""))

    @staticmethod
    def convert_kanji_yen_string_to_int(yen_string: str) -> int:
        """This method convert YEN string to int."""
        if "." in yen_string:
            msg = f"Decimal is unsupported. Yen string = {yen_string}"
            raise ValueError(msg)
        matches = re.search(r"([\d,]+)\s*円", yen_string)
        if matches is None:
            msg = f"Invalid yen string. Yen string = {yen_string}"
            raise ValueError(msg)
        return int(matches.group(1).replace(",", ""))

    @staticmethod
    def convert_symbol_yen_string_to_int(yen_string: str) -> int:
        """This method convert YEN string to int."""
        if "." in yen_string:
            msg = f"Decimal is unsupported. Yen string = {yen_string}"
            raise ValueError(msg)
        matches = re.search(r"\\([\d,]+)", yen_string)
        if matches is None:
            msg = f"Invalid yen string. Yen string = {yen_string}"
            raise ValueError(msg)
        return int(matches.group(1).replace(",", ""))

    @staticmethod
    def convert_string_with_comma_to_int(string_with_comma: str) -> int:
        return int(string_with_comma.replace(",", ""))
