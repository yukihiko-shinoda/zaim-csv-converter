"""This module implements utility."""
import re
from typing import Optional


class Utility:
    """This class implements utility."""

    @staticmethod
    def convert_string_to_int_or_none(string) -> Optional[int]:
        """This method converts string to int or None."""
        if string == "":
            return None
        return int(string.replace(",", ""))

    @staticmethod
    def convert_yen_string_to_int(yen_string: str):
        """This method convert YEN string to int."""
        if "." in yen_string:
            raise ValueError(f"Decimal is unsupported. Yen string = {yen_string}")
        matches = re.search(r"([\d,]+)円", yen_string)
        if matches is None:
            raise ValueError(f"Invalid yen string. Yen string = {yen_string}")
        return int(matches.group(1).replace(",", ""))
