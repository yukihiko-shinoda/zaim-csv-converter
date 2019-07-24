"""Tests for model."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.account import Account
from zaimcsvconverter.models import Store, StoreRowData, AccountId


class TestModel:
    """Tests for Model."""
    @staticmethod
    def test_save_all(database_session_with_schema):
        """Arguments should insert into database."""
        stores = [Store(AccountId.WAON, StoreRowData('上尾', 'イオンモール　上尾'))]
        Store.save_all(stores)
        stores = database_session_with_schema.query(Store).filter(Store.name == '上尾').one()
        assert stores.name == '上尾'
        assert stores.name_zaim == 'イオンモール　上尾'

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'database_session_with_schema, account, store_name, expected_store_name_zaim, expected_transfer_target', [
            ([InstanceResource.FIXTURE_RECORD_STORE_WAON_MAKUHARISHINTOSHIN],
             Account.WAON, '幕張新都心', 'イオンモール　幕張新都心', None),
            ([InstanceResource.FIXTURE_RECORD_STORE_MUFG_TOBU_CARD], Account.MUFG, 'カ）トウブカ－ドビ', None, '東武カード'),
        ], indirect=['database_session_with_schema'])
    def test_try_to_find_success(
            database_session_with_schema,
            account,
            store_name,
            expected_store_name_zaim,
            expected_transfer_target
    ):
        """Method should return Store model when store name is exist in database."""
        store = Store.try_to_find(account.value.id, store_name)
        assert store.name == store_name
        assert store.name_zaim == expected_store_name_zaim
        assert store.transfer_target == expected_transfer_target

    @staticmethod
    def test_try_to_find_failure(database_session_with_schema):
        """Method should raise KeyError when store name is not exist in database."""
        store = Store.try_to_find(Account.WAON.value.id, '上尾')
        assert store is None
