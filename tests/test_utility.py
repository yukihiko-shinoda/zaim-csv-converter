#!/usr/bin/env python
"""Tests for utility."""
import pytest

from zaimcsvconverter.utility import Utility


class TestUtility:
    """Tests for Account."""
    @pytest.mark.parametrize('argument, expected', [
        ('', None),
        ('1,000', 1000),
    ])
    def test_convert_string_to_int_or_none(self, argument, expected):
        """
        Method should return None when argument is empty string.
        Method should return integer even if argument include comma.
        """
        assert Utility.convert_string_to_int_or_none(argument) == expected
