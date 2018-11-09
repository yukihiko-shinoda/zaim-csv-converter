#!/usr/bin/env python

from datetime import datetime

import parameterized
import unittest2 as unittest

from zaimcsvconverter.waon.waon_payment_row import WaonPaymentRow


class TestWaonRow(unittest.TestCase):
    @parameterized.parameterized.expand([
        (['2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', '-'], (2018, 8, 7, 0, 0, 0), 129),
        (['2018/8/30', '板橋前野町', '1,489円', '支払', '-'], (2018, 8, 30, 0, 0, 0), 1489),
    ])
    def test_init(self, argument, expected_date, expected_use_amount):
        waon_row = WaonPaymentRow(argument)
        self.assertEqual(datetime(*expected_date), waon_row.date)
        self.assertEqual(argument[1], waon_row.used_store)
        self.assertEqual(expected_use_amount, waon_row.used_amount)
        self.assertEqual(argument[3], waon_row._used_kind)
        self.assertEqual(argument[4], waon_row._charge_kind)
