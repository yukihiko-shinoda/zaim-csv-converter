#!/usr/bin/env python

"""
This module implements testing utility using SQLAlchemy and factory_boy.
@see https://factoryboy.readthedocs.io/en/latest/orms.html#sqlalchemy
"""
import os
import shutil
from abc import abstractmethod
from pathlib import Path
from time import sleep

import factory
import sqlalchemy
import unittest2 as unittest

from zaimcsvconverter import Session, CONFIG
from zaimcsvconverter.models import initialize_database, Store


def create_database():
    """
    This function creates new in memory database to run unittest as parallel.
    """
    engine = sqlalchemy.create_engine('sqlite://')
    # It's a scoped_session, and now is the time to configure it.
    Session.configure(bind=engine)
    session = Session()
    initialize_database(engine)

    return session


class StoreFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for Store model."""
    class Meta:
        """Settings for factory_boy"""
        model = Store
        sqlalchemy_session = Session


class DatabaseTestCase(unittest.TestCase):
    """
    This class creates new in memory database to run unittest as parallel.
    """
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


class ConfigHandler:
    """This class handles config.yml."""
    PATH_TARGET: Path = Path(__file__).parent.parent
    PATH_SOURCE: Path = Path(__file__).parent
    FILE_TARGET: Path = PATH_TARGET / 'config.yml'
    FILE_SOURCE: Path = PATH_SOURCE / 'config.yml.dist'
    FILE_BACK_UP: Path = PATH_TARGET / 'config.yml.bak'

    @staticmethod
    def set_up():
        """This function set up config.yml."""
        if ConfigHandler.FILE_TARGET.is_file():
            shutil.move(str(ConfigHandler.FILE_TARGET), str(ConfigHandler.FILE_BACK_UP))
        shutil.copy(str(ConfigHandler.FILE_SOURCE), str(ConfigHandler.FILE_TARGET))
        CONFIG.load()

    @staticmethod
    def do_cleanups():
        """This function clean up config.yml."""
        os.unlink(str(ConfigHandler.FILE_TARGET))
        if ConfigHandler.FILE_BACK_UP.is_file():
            shutil.move(str(ConfigHandler.FILE_BACK_UP), str(ConfigHandler.FILE_TARGET))


class ConfigurableDatabaseTestCase(DatabaseTestCase):
    """
    This class creates new in memory database to run unittest as parallel,
    and also creates config.yml.
    """
    def setUp(self):
        super().setUp()
        ConfigHandler.set_up()

    @abstractmethod
    def _prepare_fixture(self):
        pass

    def doCleanups(self):
        ConfigHandler.do_cleanups()
        super().doCleanups()


class ConfigurableTestCase(unittest.TestCase):
    """
    This class creates config.yml.
    """
    def setUp(self):
        ConfigHandler.set_up()

    def doCleanups(self):
        ConfigHandler.do_cleanups()
