#!/usr/bin/env python
"""Tests for WaonRow."""
from datetime import datetime
import unittest2 as unittest

import parameterized

from tests.database_test import DatabaseTestCase, StoreFactory
from zaimcsvconverter.inputcsvformats.waon import WaonPaymentRow, WaonAutoChargeRow, WaonRowData, WaonRowFactory, \
    WaonChargeRow, WaonDownloadPointRow
from zaimcsvconverter.account import Account
from zaimcsvconverter.models import StoreRowData


class TestWaonRowData(unittest.TestCase):
    """Tests for WaonRowData."""
    def test_init_and_property(self):
        """
        Property date should return datetime object.
        Property store_date should return used_store.
        """
        date = '2018/8/7'
        used_store = 'ファミリーマートかぶと町永代'
        used_amount = '129円'
        use_kind = '支払'
        charge_kind = '-'
        waon_row_data = WaonRowData(date, used_store, used_amount, use_kind, charge_kind)
        self.assertEqual(waon_row_data.date, datetime(2018, 8, 7, 0, 0))
        self.assertEqual(waon_row_data.store_name, used_store)
        self.assertEqual(waon_row_data.used_amount, used_amount)
        self.assertEqual(waon_row_data.use_kind, use_kind)
        self.assertEqual(waon_row_data.charge_kind, charge_kind)


def prepare_fixture():
    """This function prepare common fixture with some tests."""
    StoreFactory(
        account=Account.WAON,
        row_data=StoreRowData('ファミリーマートかぶと町永代', 'ファミリーマート　かぶと町永代通り店'),
    )
    StoreFactory(
        account=Account.WAON,
        row_data=StoreRowData('板橋前野町', 'イオンスタイル　板橋前野町'),
    )


class TestWaonRow(DatabaseTestCase):
    """Tests for WaonRow."""
    def _prepare_fixture(self):
        prepare_fixture()

    # pylint: disable=too-many-arguments
    @parameterized.parameterized.expand([
        (WaonRowData('2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', '-'), datetime(2018, 8, 7, 0, 0, 0),
         'ファミリーマート　かぶと町永代通り店', 129, None),
        (WaonRowData('2018/8/30', '板橋前野町', '1,489円', '支払', '-'), datetime(2018, 8, 30, 0, 0, 0),
         'イオンスタイル　板橋前野町', 1489, None),
    ])
    def test_init_success(self, waon_row_data, expected_date, expexted_store_name_zaim, expected_use_amount,
                          expected_charge_kind):
        """
        Arguments should set into properties.
        :param WaonRowData waon_row_data:
        """
        waon_row = WaonPaymentRow(Account.WAON, waon_row_data)
        self.assertEqual(waon_row.zaim_date, expected_date)
        # pylint: disable=protected-access
        self.assertEqual(waon_row.zaim_store.name, waon_row_data._used_store)
        self.assertEqual(waon_row.zaim_store.name_zaim, expexted_store_name_zaim)
        # pylint: disable=protected-access
        self.assertEqual(waon_row._used_amount, expected_use_amount)
        # pylint: disable=protected-access
        self.assertEqual(waon_row._charge_kind, expected_charge_kind)
        # TODO 全propertyのテスト

    def test_init_fail(self):
        """Constructor should raise ValueError when got undefined charge kind."""
        with self.assertRaises(ValueError):
            WaonPaymentRow(Account.WAON, WaonRowData('2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', 'クレジットカード'))

# TODO 全具象クラスのテスト


class TestWaonRowFactory(DatabaseTestCase):
    """Tests for WaonRowFactory."""
    def _prepare_fixture(self):
        prepare_fixture()

    @parameterized.parameterized.expand([
        (WaonRowData('2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', '-'), WaonPaymentRow),
        (WaonRowData('2018/8/22', '板橋前野町', '5,000円', 'チャージ', 'ポイント'), WaonChargeRow),
        (WaonRowData('2018/8/22', '板橋前野町', '5,000円', 'オートチャージ', '銀行口座'), WaonAutoChargeRow),
        (WaonRowData('2018/8/22', '板橋前野町', '5,000円', 'ポイントダウンロード', '-'), WaonDownloadPointRow),
    ])
    def test_create_success(self, argument, expected):
        """Method should return Store model when use kind is defined."""
        # pylint: disable=protected-access
        waon_row = WaonRowFactory().create(Account.WAON, argument)
        self.assertIsInstance(waon_row, expected)

    def test_create_fail(self):
        """Method should raise ValueError when use kind is not defined."""
        with self.assertRaises(ValueError):
            # pylint: disable=protected-access
            WaonRowFactory().create(Account.WAON, WaonRowData('2018/8/7', 'ファミリーマートかぶと町永代', '10000円', '入金', '-'))
