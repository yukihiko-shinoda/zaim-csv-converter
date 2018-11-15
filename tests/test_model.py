#!/usr/bin/env python
"""Tests for model."""
from parameterized import parameterized

from tests.database_test import DatabaseTestCase, StoreFactory
from zaimcsvconverter.enum import Account
from zaimcsvconverter.models import Store


class TestModel(DatabaseTestCase):
    """Tests for Model."""
    def _prepare_fixture(self):
        StoreFactory(
            account=Account.WAON,
            list_row_store=['幕張新都心', 'イオンモール　幕張新都心'],
        )
        StoreFactory(
            account=Account.MUFG,
            list_row_store=['カ）トウブカ－ドビ', '', '', '', '', '東武カード'],
        )

    def test_save_all(self):
        """Arguments should insert into database."""
        stores = [Store(Account.WAON, ['上尾', 'イオンモール　上尾'])]
        Store.save_all(stores)
        stores = self._session.query(Store).filter(Store.name == '上尾').one()
        assert stores.name == '上尾'
        assert stores.name_zaim == 'イオンモール　上尾'

    # pylint: disable=no-self-use
    @parameterized.expand([
        (Account.WAON, '幕張新都心', 'イオンモール　幕張新都心', None),
        (Account.MUFG, 'カ）トウブカ－ドビ', None, '東武カード'),
    ])
    def test_try_to_find_success(self, account, store_name, expected_store_name_zaim, expected_transfer_target):
        """Method should return Store model when store name is exist in database."""
        store = Store.try_to_find(account, store_name)
        assert store.name == store_name
        assert store.name_zaim == expected_store_name_zaim
        assert store.transfer_target == expected_transfer_target

    def test_try_to_find_failure(self):
        """Method should raise KeyError when store name is not exist in database."""
        with self.assertRaises(KeyError):
            Store.try_to_find(Account.WAON, '上尾')
