"""Tests for utility."""

from typing import Optional

import pytest

from zaimcsvconverter.utility import Utility


class TestUtility:
    """Tests for Account."""

    @staticmethod
    @pytest.mark.parametrize(("argument", "expected"), [("", None), ("1,000", 1000)])
    def test_convert_string_to_int_or_none(argument: str, expected: Optional[int]) -> None:
        """Test following:

        - Method should return None when argument is empty string.
        - Method should return integer even if argument include comma.
        """
        assert Utility.convert_string_to_int_or_none(argument) == expected

    @staticmethod
    @pytest.mark.parametrize(("argument", "expected"), [("1,987円", 1987), ("951円", 951), ("0円", 0), ("１円", 1)])
    def test_convert_yen_string_to_int_success(argument: str, expected: int) -> None:
        """YEN string should be converted into int."""
        assert Utility.convert_kanji_yen_string_to_int(argument) == expected

    @staticmethod
    @pytest.mark.parametrize("argument", ["1,987$", "1.951円"])
    def test_convert_yen_string_to_int_fail(argument: str) -> None:
        """Invalid YEN string should be raised ValueError."""
        with pytest.raises(ValueError, match=r"\.\sYen\sstring\s\=\s"):
            Utility.convert_kanji_yen_string_to_int(argument)
