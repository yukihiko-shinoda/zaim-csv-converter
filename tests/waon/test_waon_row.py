#!/usr/bin/env python

from datetime import datetime

import parameterized

from tests.database_test import DatabaseTestCase, StoreFactory
from zaimcsvconverter.enum import Account
from zaimcsvconverter.waon.waon_payment_row import WaonPaymentRow


class TestWaonRow(DatabaseTestCase):
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
        (['2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', '-'], (2018, 8, 7, 0, 0, 0), 'ファミリーマート　かぶと町永代通り店', 129),
        (['2018/8/30', '板橋前野町', '1,489円', '支払', '-'], (2018, 8, 30, 0, 0, 0), 'イオンスタイル　板橋前野町', 1489),
    ])
    def test_init(self, argument, expected_date, expexted_store_name_zaim, expected_use_amount):
        waon_row = WaonPaymentRow(argument)
        self.assertEqual(waon_row.date, datetime(*expected_date))
        self.assertEqual(waon_row.used_store.name, argument[1])
        self.assertEqual(waon_row.used_store.name_zaim, expexted_store_name_zaim)
        self.assertEqual(waon_row.used_amount, expected_use_amount)
        self.assertEqual(waon_row._charge_kind, argument[4])
