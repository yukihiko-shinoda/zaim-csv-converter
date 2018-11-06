#!/usr/bin/env python
import factory
import unittest2 as unittest
from sqlalchemy.orm.exc import NoResultFound

from tests.common import CommonSession, create_database
from zaimcsvconverter.models import WaonStore
from zaimcsvconverter.session_manager import SessionManager


class WaonStoreFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(object):
        model = WaonStore
        sqlalchemy_session = CommonSession

    name = '幕張新都心'
    name_zaim = 'イオンモール　幕張新都心'


class TestSessionManager(unittest.TestCase):

    def setUp(self):
        self._session = create_database()
        WaonStoreFactory()

    def test_import_waon_store(self):
        waon_store = WaonStore('上尾', 'イオンモール　上尾')
        with SessionManager(self._session) as session_manager:
            session_manager.save_waon_store(waon_store)
            waon_store = self._session.query(WaonStore).filter(WaonStore.name == '上尾').one()
            assert waon_store.name == '上尾'
            assert waon_store.name_zaim == 'イオンモール　上尾'

    def test_find_waon_store_success(self):
        with SessionManager(self._session) as session_manager:
            waon_store = session_manager.find_waon_store('幕張新都心')
            assert waon_store.name == '幕張新都心'
            assert waon_store.name_zaim == 'イオンモール　幕張新都心'

    def test_find_waon_store_failure(self):
        with self.assertRaises(NoResultFound):
            with SessionManager(self._session) as session_manager:
                session_manager.find_waon_store('上尾')

    def doCleanups(self):
        # Remove it, so that the next test gets a new Session()
        CommonSession.remove()
