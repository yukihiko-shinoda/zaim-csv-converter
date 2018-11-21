#!/usr/bin/env python
"""Tests for GoldPointCartPlusRow."""
from datetime import datetime

import parameterized

from tests.database_test import StoreFactory, DatabaseTestCase
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRow, GoldPointCardPlusRowData
from zaimcsvconverter.models import Store, StoreRowData


class TestGoldPointCardPlusRow(DatabaseTestCase):
    """Tests for GoldPointCartPlusRow."""
    def _prepare_fixture(self):
        StoreFactory(
            account=Account.GOLD_POINT_CARD_PLUS,
            row_data=StoreRowData('東京電力  電気料金等', '東京電力エナジーパートナー株式会社'),
        )
        StoreFactory(
            account=Account.GOLD_POINT_CARD_PLUS,
            row_data=StoreRowData('ＡＭＡＺＯＮ．ＣＯ．ＪＰ', 'Amazon Japan G.K.'),
        )

    # pylint: disable=protected-access,too-many-arguments
    @parameterized.parameterized.expand([
        (
            GoldPointCardPlusRowData(
                '2018/7/3',
                '東京電力  電気料金等',
                'ご本人',
                '1回払い', '', '18/8', '11402', '11402',
                '', '', '', '', ''),
            datetime(2018, 7, 3, 0, 0, 0), '東京電力エナジーパートナー株式会社', 1, 11402),
        (
            GoldPointCardPlusRowData(
                '2018/7/4',
                'ＡＭＡＺＯＮ．ＣＯ．ＪＰ',
                'ご本人',
                '1回払い',
                '',
                '18/8',
                '3456',
                '3456',
                '', '', '', '', ''),
            datetime(2018, 7, 4, 0, 0, 0), 'Amazon Japan G.K.', 1, 3456),
    ])
    def test_init(self,
                  gold_point_card_plus_row_data,
                  expected_date,
                  expected_store_name_zaim,
                  expected_number_of_division,
                  expected_use_amount
                  ):
        """
        Arguments should set into properties.
        :param GoldPointCardPlusRowData gold_point_card_plus_row_data:
        """
        row = GoldPointCardPlusRow(Account.GOLD_POINT_CARD_PLUS, gold_point_card_plus_row_data)
        self.assertEqual(row.zaim_date, expected_date)
        self.assertIsInstance(row.zaim_store, Store)
        self.assertEqual(row.zaim_store.name, gold_point_card_plus_row_data._used_store)
        self.assertEqual(row.zaim_store.name_zaim, expected_store_name_zaim)
        self.assertEqual(row._used_card, gold_point_card_plus_row_data.used_card)
        self.assertEqual(row._payment_kind, gold_point_card_plus_row_data.payment_kind)
        self.assertEqual(row._number_of_division, expected_number_of_division)
        self.assertEqual(row._scheduled_payment_month, gold_point_card_plus_row_data.scheduled_payment_month)
        self.assertEqual(row._used_amount, expected_use_amount)
