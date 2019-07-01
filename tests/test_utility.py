#!/usr/bin/env python
"""Tests for utility."""
import unittest2 as unittest
from parameterized import parameterized

from zaimcsvconverter.utility import Utility


class TestUtility(unittest.TestCase):
    """Tests for Account."""
    @parameterized.expand([
        ('', None),
        ('1,000', 1000),
    ])
    def test_convert_string_to_int_or_none(self, argument, expected):
        """
        Method should return None when argument is empty string.
        Method should return integer even if argument include comma.
        """
        self.assertEqual(Utility.convert_string_to_int_or_none(argument), expected)
