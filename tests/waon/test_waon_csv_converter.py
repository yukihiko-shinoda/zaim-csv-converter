#!/usr/bin/env python

import parameterized
import unittest2 as unittest

from zaimcsvconverter.waon.waon_auto_charge_row import WaonAutoChargeRow
from zaimcsvconverter.waon.waon_csv_converter import WaonCsvConverter
from zaimcsvconverter.waon.waon_payment_row import WaonPaymentRow


class TestWaonCsvConverter(unittest.TestCase):
    @parameterized.parameterized.expand([
        (['2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', '-'], WaonPaymentRow),
        (['2018/8/22', '板橋前野町', '5,000円', 'オートチャージ', '銀行口座'], WaonAutoChargeRow),
    ])
    def test_create_success(self, argument, expected):
        waon_csv_converter = WaonCsvConverter('')
        waon_row = waon_csv_converter._create_account_row(argument)
        self.assertIsInstance(waon_row, expected)

    def test_create_fail(self):
        waon_csv_converter = WaonCsvConverter('')
        with self.assertRaises(NotImplementedError):
            waon_csv_converter._create_account_row(['2018/8/7', 'ファミリーマートかぶと町永代', '10000円', '入金', '-'])
