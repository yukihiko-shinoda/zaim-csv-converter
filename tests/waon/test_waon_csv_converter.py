#!/usr/bin/env python

import parameterized

from tests.database_test import DatabaseTestCase, StoreFactory
from zaimcsvconverter.enum import Account
from zaimcsvconverter.waon.waon_auto_charge_row import WaonAutoChargeRow
from zaimcsvconverter.waon.waon_csv_converter import WaonCsvConverter
from zaimcsvconverter.waon.waon_payment_row import WaonPaymentRow


class TestWaonCsvConverter(DatabaseTestCase):
    def _prepare_fixture(self):
        StoreFactory(
            account=Account.WAON,
            list_row_store=['ファミリーマートかぶと町永代', 'ファミリーマート　かぶと町永代通り店'],
        )
        StoreFactory(
            account=Account.WAON,
            list_row_store=['板橋前野町', 'イオンスタイル　板橋前野町'],
        )

    @parameterized.parameterized.expand([
        (['2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', '-'], WaonPaymentRow),
        (['2018/8/22', '板橋前野町', '5,000円', 'オートチャージ', '銀行口座'], WaonAutoChargeRow),
    ])
    def test_create_success(self, argument, expected):
        waon_row = WaonCsvConverter._create_account_row(argument)
        self.assertIsInstance(waon_row, expected)

    def test_create_fail(self):
        with self.assertRaises(NotImplementedError):
            WaonCsvConverter._create_account_row(['2018/8/7', 'ファミリーマートかぶと町永代', '10000円', '入金', '-'])
