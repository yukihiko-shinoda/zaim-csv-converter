#!/usr/bin/env python
"""Tests for GoldPointCartPlusRow."""
from datetime import datetime

import parameterized

from tests.database_test import StoreFactory, DatabaseTestCase
from zaimcsvconverter.enum import Account
from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_row import GoldPointCardPlusRow
from zaimcsvconverter.models import Store


class TestGoldPointCardPlusRow(DatabaseTestCase):
    """Tests for GoldPointCartPlusRow."""
    def _prepare_fixture(self):
        StoreFactory(
            account=Account.GOLD_POINT_CARD_PLUS,
            list_row_store=['東京電力  電気料金等', '東京電力エナジーパートナー株式会社'],
        )
        StoreFactory(
            account=Account.GOLD_POINT_CARD_PLUS,
            list_row_store=['ＡＭＡＺＯＮ．ＣＯ．ＪＰ', 'Amazon Japan G.K.'],
        )

    # pylint: disable=protected-access,too-many-arguments
    @parameterized.parameterized.expand([
        (['2018/7/3', '東京電力  電気料金等', 'ご本人', '1回払い', '', '18/8', '11402', '11402'], (2018, 7, 3, 0, 0, 0),
         '東京電力エナジーパートナー株式会社', 1, 11402),
        (['2018/7/4', 'ＡＭＡＺＯＮ．ＣＯ．ＪＰ', 'ご本人', '1回払い', '', '18/8', '3456', '3456'], (2018, 7, 4, 0, 0, 0),
         'Amazon Japan G.K.', 1, 3456),
    ])
    def test_init(self,
                  argument,
                  expected_date,
                  expected_store_name_zaim,
                  expected_number_of_division,
                  expected_use_amount
                  ):
        """Arguments should set into properties."""
        row = GoldPointCardPlusRow(argument)
        self.assertEqual(row.zaim_date, datetime(*expected_date))
        self.assertIsInstance(row.zaim_store, Store)
        self.assertEqual(row.zaim_store.name, argument[1])
        self.assertEqual(row.zaim_store.name_zaim, expected_store_name_zaim)
        self.assertEqual(row._used_card, argument[2])
        self.assertEqual(row._payment_kind, argument[3])
        self.assertEqual(row._number_of_division, expected_number_of_division)
        self.assertEqual(row._scheduled_payment_month, argument[5])
        self.assertEqual(row._used_amount, expected_use_amount)
