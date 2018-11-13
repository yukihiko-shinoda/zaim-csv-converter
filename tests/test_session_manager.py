#!/usr/bin/env python
import parameterized

from tests.database_test import StoreFactory, DatabaseTestCase
from zaimcsvconverter.enum import Account
from zaimcsvconverter.models import Store


class TestSessionManager(DatabaseTestCase):
    def _prepare_fixture(self):
        StoreFactory(
            account=Account.WAON,
            list_row_store=['幕張新都心', 'イオンモール　幕張新都心'],
        )
        StoreFactory(
            account=Account.MUFG,
            list_row_store=['カ）トウブカ－ドビ', '', '', '', '', '東武カード'],
        )

    def test_import_stores(self):
        stores = [Store(Account.WAON, ['上尾', 'イオンモール　上尾'])]
        Store.save_all(stores)
        stores = self._session.query(Store).filter(Store.name == '上尾').one()
        assert stores.name == '上尾'
        assert stores.name_zaim == 'イオンモール　上尾'

    @parameterized.parameterized.expand([
        (Account.WAON, '幕張新都心', 'イオンモール　幕張新都心', None),
        (Account.MUFG, 'カ）トウブカ－ドビ', None, '東武カード'),
    ])
    def test_find_waon_store_success(self, account, store_name, expected_store_name_zaim, expected_transfer_target):
        store = Store.try_to_find(account, store_name)
        assert store.name == store_name
        assert store.name_zaim == expected_store_name_zaim
        assert store.transfer_target == expected_transfer_target

    def test_find_waon_store_failure(self):
        with self.assertRaises(KeyError):
                Store.try_to_find(Account.WAON, '上尾')
