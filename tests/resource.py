#!/usr/bin/env python

"""
This module implements testing utility using SQLAlchemy and factory_boy.
@see https://factoryboy.readthedocs.io/en/latest/orms.html#sqlalchemy
"""
import os
import re
import shutil
import sys
from abc import abstractmethod
from pathlib import Path
from typing import Union, Type

import factory
import sqlalchemy
import unittest2 as unittest

from zaimcsvconverter import Session, CONFIG
from zaimcsvconverter.models import initialize_database, Store, Item


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


class ItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for Store model."""
    class Meta:
        """Settings for factory_boy"""
        model = Item
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
    def set_up(file_source=FILE_SOURCE):
        """This function set up config.yml."""
        if ConfigHandler.FILE_TARGET.is_file():
            shutil.move(str(ConfigHandler.FILE_TARGET), str(ConfigHandler.FILE_BACK_UP))
        shutil.copy(str(file_source), str(ConfigHandler.FILE_TARGET))
        CONFIG.load()

    @staticmethod
    def do_cleanups():
        """This function clean up config.yml."""
        if ConfigHandler.FILE_BACK_UP.is_file():
            os.unlink(str(ConfigHandler.FILE_TARGET))
            shutil.move(str(ConfigHandler.FILE_BACK_UP), str(ConfigHandler.FILE_TARGET))


def create_path_as_same_as_file_name(argument: Union[object, Type[object]]) -> Path:
    """This function creates and returns path as same as file name."""
    if isinstance(argument, object):
        argument = argument.__class__
    return Path(re.search(r'(.*)\.py', sys.modules[argument.__module__].__file__).group(1))


class ConfigurableDatabaseTestCase(DatabaseTestCase):
    """
    This class creates new in memory database to run unittest as parallel,
    and also creates config.yml.
    """
    def setUp(self):
        super().setUp()
        if self.source_yaml_file is None:
            ConfigHandler.set_up()
        else:
            ConfigHandler.set_up(create_path_as_same_as_file_name(self) / self.source_yaml_file)

    @abstractmethod
    def _prepare_fixture(self):
        pass

    def doCleanups(self):
        ConfigHandler.do_cleanups()
        super().doCleanups()

    @property
    def source_yaml_file(self) -> Union[str, None]:
        """This property returns source yaml file"""
        return None


class ConfigurableTestCase(unittest.TestCase):
    """
    This class creates config.yml.
    """
    def setUp(self):
        if self.source_yaml_file is None:
            ConfigHandler.set_up()
        else:
            ConfigHandler.set_up(create_path_as_same_as_file_name(self) / self.source_yaml_file)

    def doCleanups(self):
        ConfigHandler.do_cleanups()

    @property
    def source_yaml_file(self) -> Union[str, None]:
        """This property returns source yaml file"""
        return None


class CsvHandler:
    """This class handles CSV."""
    PATH_TARGET_OUTPUT: Path = Path(__file__).parent.parent / 'csvoutput'

    @staticmethod
    def set_up(file_source: Path):
        """This function set up CSV."""
        file_target_output = CsvHandler.__file_target_output(file_source)
        file_back_up_output = CsvHandler.__file_back_up_output(file_source)
        if file_target_output.is_file():
            shutil.move(str(file_target_output), str(file_back_up_output))
        CONFIG.load()

    @staticmethod
    def do_cleanups(file_source: Path):
        """This function clean up CSV."""
        file_target_output = CsvHandler.__file_target_output(file_source)
        file_back_up_output = CsvHandler.__file_back_up_output(file_source)
        if file_back_up_output.is_file():
            os.unlink(str(file_target_output))
            shutil.move(str(file_back_up_output), str(file_target_output))

    @staticmethod
    def __file_target_output(file_source: Path):
        return CsvHandler.PATH_TARGET_OUTPUT / file_source.name

    @staticmethod
    def __file_back_up_output(file_source: Path):
        return CsvHandler.PATH_TARGET_OUTPUT / (file_source.name + '.bak')
