# @see https://factoryboy.readthedocs.io/en/latest/orms.html#sqlalchemy
from abc import abstractmethod

import factory
import sqlalchemy
import unittest2 as unittest

from zaimcsvconverter import Session
from zaimcsvconverter.models import initialize_database, Store


def create_database():
    # ↓ To run unittest as parallel
    engine = sqlalchemy.create_engine('sqlite://')
    # It's a scoped_session, and now is the time to configure it.
    Session.configure(bind=engine)
    session = Session()
    initialize_database(engine)

    return session


class StoreFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Store
        sqlalchemy_session = Session


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self._session = create_database()
        self._prepare_fixture()
        self._session.flush()

    @abstractmethod
    def _prepare_fixture(self):
        pass

    def doCleanups(self):
        # Remove it, so that the next test gets a new Session()
        Session.remove()
