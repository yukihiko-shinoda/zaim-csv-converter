#!/usr/bin/env python
from datetime import datetime

import parameterized
import unittest2 as unittest

from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_row import GoldPointCardPlusRow


class TestGoldPointCardPlusRow(unittest.TestCase):
    @parameterized.parameterized.expand([
        (['2018/7/3', '東京電力  電気料金等', 'ご本人', '1回払い', '', '18/8', '11402', '11402'], (2018, 7, 3, 0, 0, 0), 1, 11402),
        (['2018/7/4', 'ＡＭＡＺＯＮ．ＣＯ．ＪＰ', 'ご本人', '1回払い', '', '18/8', '3456', '3456'], (2018, 7, 4, 0, 0, 0), 1, 3456),
    ])
    def test_init(self, argument, expected_date, expected_number_of_division, expected_use_amount):
        row = GoldPointCardPlusRow(argument)
        self.assertEqual(datetime(*expected_date), row.used_date)
        self.assertEqual(argument[1], row.used_store)
        self.assertEqual(argument[2], row._used_card)
        self.assertEqual(argument[3], row._payment_kind)
        self.assertEqual(expected_number_of_division, row._number_of_division)
        self.assertEqual(argument[5], row._scheduled_payment_month)
        self.assertEqual(expected_use_amount, row.used_amount)
