#!/usr/bin/env python
"""Tests for error_handler.py."""
import unittest2 as unittest

from tests.instance_fixture import InstanceFixture
from zaimcsvconverter.account import Account
from zaimcsvconverter.error_handler import ErrorHandler


class TestErrorHandler(unittest.TestCase):
    """Tests for ErrorHandler"""
    def test_init_is_presented_false(self):
        """list_error should be empty when initialized."""
        self.assertEqual(ErrorHandler().is_presented, False)

    def test_append_undefined_content_extend_is_presented_true_uniquify_iter(self):
        """Instance should be iterable."""
        error_amazon = ['amazon.csv', '', 'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト']
        error_waon = ['waon.csv', 'ファミリーマートかぶと町永代', '']
        error_handler_a = ErrorHandler()
        error_handler_a.append_undefined_content(Account.WAON, InstanceFixture.ROW_DATA_WAON)
        self.assertEqual(error_handler_a.list_error, [error_waon])
        error_handler_b = ErrorHandler()
        error_handler_b.append_undefined_content(Account.AMAZON, InstanceFixture.ROW_DATA_AMAZON)
        error_handler_b.append_undefined_content(Account.AMAZON, InstanceFixture.ROW_DATA_AMAZON)
        self.assertEqual(error_handler_b.list_error, [error_amazon, error_amazon])
        error_handler_a.extend(error_handler_b)
        self.assertEqual(error_handler_a.list_error, [error_waon, error_amazon, error_amazon])
        self.assertEqual(error_handler_a.is_presented, True)
        error_handler_a.uniquify()
        list_error = [error_amazon, error_waon]
        index = 0
        for error_row in error_handler_a:
            self.assertEqual(error_row, list_error[index])
            index += 1
        self.assertEqual(index, 2)
