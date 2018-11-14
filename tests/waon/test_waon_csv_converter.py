#!/usr/bin/env python

import parameterized

from tests.database_test import DatabaseTestCase
from tests.waon import prepare_fixture
from zaimcsvconverter.waon.waon_auto_charge_row import WaonAutoChargeRow
from zaimcsvconverter.waon.waon_csv_converter import WaonCsvConverter
from zaimcsvconverter.waon.waon_payment_row import WaonPaymentRow


class TestWaonCsvConverter(DatabaseTestCase):
    def _prepare_fixture(self):
        prepare_fixture()

    @parameterized.parameterized.expand([
        (['2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', '-'], WaonPaymentRow),
        (['2018/8/22', '板橋前野町', '5,000円', 'オートチャージ', '銀行口座'], WaonAutoChargeRow),
    ])
    def test_create_success(self, argument, expected):
        # pylint: disable=protected-access
        waon_row = WaonCsvConverter._create_account_row(argument)
        self.assertIsInstance(waon_row, expected)

    def test_create_fail(self):
        with self.assertRaises(NotImplementedError):
            # pylint: disable=protected-access
            WaonCsvConverter._create_account_row(['2018/8/7', 'ファミリーマートかぶと町永代', '10000円', '入金', '-'])
