"""Tests for model."""
import pytest

from tests.testlibraries.database import StoreFactory
from tests.conftest import database_session_with_records
from zaimcsvconverter.account import Account
from zaimcsvconverter.models import Store, StoreRowData


@pytest.fixture
def database_session_store():
    """This fixture prepares database session and records."""
    def fixture_records():
        StoreFactory(
            account=Account.WAON,
            row_data=StoreRowData('幕張新都心', 'イオンモール　幕張新都心'),
        )
        StoreFactory(
            account=Account.MUFG,
            row_data=StoreRowData('カ）トウブカ－ドビ', '', '', '', '', '東武カード'),
        )
    yield from database_session_with_records(fixture_records)


class TestModel:
    """Tests for Model."""
    @staticmethod
    def test_save_all(database_session_store):
        """Arguments should insert into database."""
        stores = [Store(Account.WAON, StoreRowData('上尾', 'イオンモール　上尾'))]
        Store.save_all(stores)
        stores = database_session_store.query(Store).filter(Store.name == '上尾').one()
        assert stores.name == '上尾'
        assert stores.name_zaim == 'イオンモール　上尾'

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize('account, store_name, expected_store_name_zaim, expected_transfer_target', [
        (Account.WAON, '幕張新都心', 'イオンモール　幕張新都心', None),
        (Account.MUFG, 'カ）トウブカ－ドビ', None, '東武カード'),
    ])
    def test_try_to_find_success(
            account,
            store_name,
            expected_store_name_zaim,
            expected_transfer_target,
            database_session_store
    ):
        """Method should return Store model when store name is exist in database."""
        store = Store.try_to_find(account, store_name)
        assert store.name == store_name
        assert store.name_zaim == expected_store_name_zaim
        assert store.transfer_target == expected_transfer_target

    @staticmethod
    def test_try_to_find_failure(database_session_store):
        """Method should raise KeyError when store name is not exist in database."""
        store = Store.try_to_find(Account.WAON, '上尾')
        assert store is None
