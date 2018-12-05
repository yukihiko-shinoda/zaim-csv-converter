#!/usr/bin/env python
"""Tests for WaonRow."""
from datetime import datetime
import unittest2 as unittest

from parameterized import parameterized

from tests.resource import DatabaseTestCase, StoreFactory, ConfigurableDatabaseTestCase
from zaimcsvconverter.inputcsvformats.waon import WaonPaymentRow, WaonAutoChargeRow, WaonRowData, WaonRowFactory, \
    WaonChargeRow, WaonDownloadPointRow
from zaimcsvconverter.account import Account
from zaimcsvconverter.models import StoreRowData, Store
from zaimcsvconverter.zaim_row import ZaimPaymentRow, ZaimIncomeRow, ZaimTransferRow


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


class TestWaonRow(ConfigurableDatabaseTestCase):
    """Tests for WaonRow."""
    def _prepare_fixture(self):
        prepare_fixture()

    # pylint: disable=too-many-arguments
    @parameterized.expand([
        (WaonRowData('2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', '-'), datetime(2018, 8, 7, 0, 0, 0),
         'ファミリーマート　かぶと町永代通り店', 129, None),
        (WaonRowData('2018/8/30', '板橋前野町', '1,489円', '支払', '-'), datetime(2018, 8, 30, 0, 0, 0),
         'イオンスタイル　板橋前野町', 1489, None),
    ])
    def test_init_success(self, waon_row_data, expected_date, expected_store_name_zaim,
                          expected_amount, expected_charge_kind):
        """
        Arguments should set into properties.
        :param WaonRowData waon_row_data:
        """
        config_account_name = 'WAON'
        config_auto_charge_source = 'イオン銀行'
        waon_row = WaonPaymentRow(Account.WAON, waon_row_data)
        self.assertEqual(waon_row.zaim_date, expected_date)
        self.assertIsInstance(waon_row.zaim_store, Store)
        self.assertEqual(waon_row.zaim_store.name_zaim, expected_store_name_zaim)
        self.assertEqual(waon_row.zaim_income_cash_flow_target, config_account_name)
        self.assertEqual(waon_row.zaim_income_ammount_income, expected_amount)
        self.assertEqual(waon_row.zaim_payment_cash_flow_source, config_account_name)
        self.assertEqual(waon_row.zaim_payment_amount_payment, expected_amount)
        self.assertEqual(waon_row.zaim_transfer_cash_flow_source, config_auto_charge_source)
        self.assertEqual(waon_row.zaim_transfer_cash_flow_target, config_account_name)
        self.assertEqual(waon_row.zaim_transfer_amount_transfer, expected_amount)
        # pylint: disable=protected-access
        self.assertEqual(waon_row._charge_kind, expected_charge_kind)

    def test_init_fail(self):
        """Constructor should raise ValueError when got undefined charge kind."""
        with self.assertRaises(ValueError):
            WaonPaymentRow(Account.WAON, WaonRowData('2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', 'クレジットカード'))


class TestWaonPaymentRow(ConfigurableDatabaseTestCase):
    """Tests for WaonPaymentRow."""
    def _prepare_fixture(self):
        prepare_fixture()

    def test_convert_to_zaim_row(self):
        """WaonPaymentRow should convert to ZaimPaymentRow."""
        waon_row = WaonPaymentRow(Account.WAON,
                                  WaonRowData('2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', '-'))
        self.assertIsInstance(waon_row.convert_to_zaim_row(), ZaimPaymentRow)


class TestWaonChargeRow(ConfigurableDatabaseTestCase):
    """Tests for WaonChargeRow."""
    def _prepare_fixture(self):
        prepare_fixture()

    @parameterized.expand([
        (WaonRowData('2018/10/22', '板橋前野町', '1,504円', 'チャージ', 'ポイント'), ZaimIncomeRow),
        (WaonRowData('2018/11/11', '板橋前野町', '5,000円', 'チャージ', '銀行口座'), ZaimTransferRow),
    ])
    def test_convert_to_zaim_row(self, waon_row_data, zaim_row_class):
        """
        WaonChargeRow for point should convert to ZaimIncomeRow.
        WaonChargeRow for bank account should convert to ZaimTransferRow.
        """
        waon_row = WaonChargeRow(Account.WAON, waon_row_data)
        self.assertIsInstance(waon_row.convert_to_zaim_row(), zaim_row_class)


class TestWaonAutoChargeRow(ConfigurableDatabaseTestCase):
    """Tests for WaonAutoChargeRow."""
    def _prepare_fixture(self):
        prepare_fixture()

    def test_convert_to_zaim_row(self):
        """WaonAutoChargeRow should convert to ZaimTransferRow."""
        waon_row = WaonAutoChargeRow(Account.WAON,
                                     WaonRowData('2018/11/11', '板橋前野町', '5,000円', 'オートチャージ', '銀行口座'))
        self.assertIsInstance(waon_row.convert_to_zaim_row(), ZaimTransferRow)


class TestWaonDownloadPointRow(DatabaseTestCase):
    """Tests for WaonDownloadPointRow."""
    waon_row = None

    def _prepare_fixture(self):
        prepare_fixture()
        self.waon_row = WaonDownloadPointRow(Account.WAON,
                                             WaonRowData('2018/10/22', '板橋前野町', '0円', 'ポイントダウンロード', '-'))

    def test_convert_to_zaim_row(self):
        """WaonDownloadPointRow should raise ValueError when convert to ZaimRow."""
        with self.assertRaises(ValueError):
            self.waon_row.convert_to_zaim_row()

    def test_is_row_to_skip(self):
        """WaonDownloadPointRow should be row to skip."""
        self.assertTrue(self.waon_row.is_row_to_skip)


class TestWaonRowFactory(DatabaseTestCase):
    """Tests for WaonRowFactory."""
    def _prepare_fixture(self):
        prepare_fixture()

    @parameterized.expand([
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
