"""This module implements utility."""
from typing import Optional


class Utility:
    """This class implements utility."""
    @staticmethod
    def convert_string_to_int_or_none(string) -> Optional[int]:
        """This method converts string to int or None."""
        if string == '':
            return None
        return int(string.replace(',', ''))
