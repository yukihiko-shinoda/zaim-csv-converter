#!/usr/bin/env python
"""Tests for GoldPointCartPlusRow."""
from datetime import datetime
import unittest2 as unittest
from parameterized import parameterized

from tests.resource import StoreFactory, DatabaseTestCase, ConfigurableDatabaseTestCase
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRow, GoldPointCardPlusRowData, \
    GoldPointCardPlusRowFactory
from zaimcsvconverter.models import Store, StoreRowData
from zaimcsvconverter.zaim_row import ZaimPaymentRow


class TestGoldPointCardPlusRowData(unittest.TestCase):
    """Tests for GoldPointCardPlusRowData."""

    # pylint: disable=too-many-locals
    def test_init_and_property(self):
        """
        Property date should return datetime object.
        Property store_date should return used_store.
        """
        used_date = '2018/7/3'
        used_store = '東京電力  電気料金等'
        used_card = 'ご本人'
        payment_kind = '1回払い'
        number_of_division = ''
        scheduled_payment_month = '18/8'
        used_amount = '11402'
        unknown_1 = '11402'
        unknown_2 = 'unknown 2'
        unknown_3 = 'unknown 3'
        unknown_4 = 'unknown 4'
        unknown_6 = 'unknown 5'
        unknown_5 = 'unknown 6'
        gold_point_card_plus_row_data = GoldPointCardPlusRowData(used_date, used_store, used_card, payment_kind,
                                                                 number_of_division, scheduled_payment_month,
                                                                 used_amount, unknown_1, unknown_2, unknown_3,
                                                                 unknown_4, unknown_5, unknown_6)
        self.assertEqual(gold_point_card_plus_row_data.used_card, used_card)
        self.assertEqual(gold_point_card_plus_row_data.payment_kind, payment_kind)
        self.assertEqual(gold_point_card_plus_row_data.number_of_division, number_of_division)
        self.assertEqual(gold_point_card_plus_row_data.scheduled_payment_month, scheduled_payment_month)
        self.assertEqual(gold_point_card_plus_row_data.used_amount, used_amount)
        self.assertEqual(gold_point_card_plus_row_data.unknown_1, unknown_1)
        self.assertEqual(gold_point_card_plus_row_data.unknown_2, unknown_2)
        self.assertEqual(gold_point_card_plus_row_data.unknown_3, unknown_3)
        self.assertEqual(gold_point_card_plus_row_data.unknown_4, unknown_4)
        self.assertEqual(gold_point_card_plus_row_data.unknown_5, unknown_5)
        self.assertEqual(gold_point_card_plus_row_data.unknown_6, unknown_6)
        self.assertEqual(gold_point_card_plus_row_data.date, datetime(2018, 7, 3, 0, 0))
        self.assertEqual(gold_point_card_plus_row_data.store_name, used_store)


def prepare_fixture():
    """This function prepare common fixture with some tests."""
    StoreFactory(
        account=Account.GOLD_POINT_CARD_PLUS,
        row_data=StoreRowData('東京電力  電気料金等', '東京電力エナジーパートナー株式会社'),
    )
    StoreFactory(
        account=Account.GOLD_POINT_CARD_PLUS,
        row_data=StoreRowData('ＡＭＡＺＯＮ．ＣＯ．ＪＰ', 'Amazon Japan G.K.'),
    )


class TestGoldPointCardPlusRow(ConfigurableDatabaseTestCase):
    """Tests for GoldPointCartPlusRow."""
    def _prepare_fixture(self):
        prepare_fixture()

    # pylint: disable=protected-access,too-many-arguments
    @parameterized.expand([
        (
            GoldPointCardPlusRowData(
                '2018/7/3',
                '東京電力  電気料金等',
                'ご本人',
                '1回払い', '', '18/8', '11402', '11402',
                '', '', '', '', ''),
            datetime(2018, 7, 3, 0, 0, 0), '東京電力エナジーパートナー株式会社', 1, 11402, False),
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
            datetime(2018, 7, 4, 0, 0, 0), 'Amazon Japan G.K.', 1, 3456, True),
    ])
    def test_init(self,
                  gold_point_card_plus_row_data,
                  expected_date,
                  expected_store_name_zaim,
                  expected_number_of_division,
                  expected_use_amount,
                  expected_is_row_to_skip
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
        self.assertEqual(row.is_row_to_skip, expected_is_row_to_skip)
        self.assertEqual(row.zaim_payment_cash_flow_source, 'ヨドバシゴールドポイントカード・プラス')
        self.assertEqual(row.zaim_payment_amount_payment, expected_use_amount)

    def test_convert_to_zaim_row(self):
        """GoldPointCardPlusRow should convert to ZaimPaymentRow."""
        sf_card_viewer_row = GoldPointCardPlusRow(
            Account.GOLD_POINT_CARD_PLUS,
            GoldPointCardPlusRowData('2018/11/2', '東京電力  電気料金等', 'ご本人', '1回払い', '', '18/12', '10997',
                                     '10997', '', '', '', '', '')
        )
        self.assertIsInstance(sf_card_viewer_row.convert_to_zaim_row(), ZaimPaymentRow)


class TestGoldPointCardPlusRowFactory(DatabaseTestCase):
    """Tests for GoldPointCardPlusRowFactory."""

    def _prepare_fixture(self):
        prepare_fixture()

    @parameterized.expand([
        (GoldPointCardPlusRowData('2018/11/2', '東京電力  電気料金等', 'ご本人', '1回払い', '', '18/12', '10997', '10997',
                                  '', '', '', '', ''),
         GoldPointCardPlusRow),
    ])
    def test_create(self, argument, expected):
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        gold_point_card_plus_row = GoldPointCardPlusRowFactory().create(Account.MUFG, argument)
        self.assertIsInstance(gold_point_card_plus_row, expected)
