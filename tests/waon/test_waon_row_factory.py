#!/usr/bin/env python

import parameterized
import unittest2 as unittest

from zaimcsvconverter.waon.waon_auto_charge_row import WaonAutoChargeRow
from zaimcsvconverter.waon.waon_payment_row import WaonPaymentRow
from zaimcsvconverter.waon.waon_row_factory import WaonRowFactory


class TestWaonRowFactory(unittest.TestCase):
    @parameterized.parameterized.expand([
        (['2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', '-'], WaonPaymentRow),
        (['2018/8/22', '板橋前野町', '5,000円', 'オートチャージ', '銀行口座'], WaonAutoChargeRow),
    ])
    def test_create_success(self, argument, expected):
        waon_row = WaonRowFactory.create(argument)
        self.assertIsInstance(waon_row, expected)

    def test_create_fail(self):
        with self.assertRaises(NotImplementedError):
            WaonRowFactory.create(['2018/8/7', 'ファミリーマートかぶと町永代', '10000円', '入金', '-'])
