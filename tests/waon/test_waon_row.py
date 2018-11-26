#!/usr/bin/env python
"""Tests for WaonRow."""
from datetime import datetime

import parameterized

from tests.database_test import DatabaseTestCase
from tests.waon import prepare_fixture
from zaimcsvconverter.inputcsvformats.waon import WaonPaymentRow, WaonAutoChargeRow, WaonRowData, WaonRowFactory
from zaimcsvconverter.account import Account


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
    def test_init(self, waon_row_data, expected_date, expexted_store_name_zaim, expected_use_amount,
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

    @parameterized.parameterized.expand([
        (WaonRowData('2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', '-'), WaonPaymentRow),
        (WaonRowData('2018/8/22', '板橋前野町', '5,000円', 'オートチャージ', '銀行口座'), WaonAutoChargeRow),
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
