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
from typing import Union, Type, NoReturn

import factory
import pytest
import sqlalchemy
from yamldataclassconfig.config_handler import YamlDataClassConfigHandler, ConfigFilePathBuilder

from zaimcsvconverter import Session, CONFIG
from zaimcsvconverter.account import Account
from zaimcsvconverter.models import initialize_database, Store, Item, StoreRowData


def create_database():
    """
    This function creates new in memory database to run unit testing as parallel.
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


class DatabaseTestCase:
    """
    This class creates new in memory database to run unit testing as parallel.
    """

    @pytest.fixture(autouse=True)
    def database_session(self):
        """This fixture prepares database and fixture records."""
        session = create_database()
        self._prepare_fixture()
        session.flush()
        yield session
        # Remove it, so that the next test gets a new Session()
        Session.remove()

    @abstractmethod
    def _prepare_fixture(self):
        pass


class ConfigHandler(YamlDataClassConfigHandler):
    """This class handles config.yml."""
    CONFIG_FILE_PATH = ConfigFilePathBuilder(path_target_directory=Path(__file__).parent.parent)


def create_path_as_same_as_file_name(argument: Union[object, Type[object]]) -> Path:
    """This function creates and returns path as same as file name."""
    if isinstance(argument, object):
        argument = argument.__class__
    return Path(re.search(r'(.*)\.py', sys.modules[argument.__module__].__file__).group(1))


def clean_up_directory(path_to_directory: Path) -> NoReturn:
    """This function cleans up content in specified directory."""
    for file in path_to_directory.rglob('*[!.gitkeep]'):
        os.unlink(str(file))


class ConfigurableDatabaseTestCase(DatabaseTestCase):
    """
    This class creates new in memory database to run unit testing as parallel,
    and also creates config.yml.
    """
    @pytest.fixture(autouse=True)
    def yaml_config(self):
        """This fixture prepares YAML config file and loads it."""
        if self.source_yaml_file is None:
            ConfigHandler.set_up()
        else:
            ConfigHandler.set_up(create_path_as_same_as_file_name(self) / self.source_yaml_file)
        CONFIG.load()
        yield
        ConfigHandler.do_cleanups()

    @abstractmethod
    def _prepare_fixture(self):
        pass

    @property
    def source_yaml_file(self) -> Union[str, None]:
        """This property returns source yaml file"""
        return None


class ConfigurableTestCase:
    """
    This class creates config.yml.
    """
    @pytest.fixture(autouse=True)
    def yaml_config(self):
        """This fixture prepares YAML config file and loads it."""
        if self.source_yaml_file is None:
            ConfigHandler.set_up()
        else:
            ConfigHandler.set_up(create_path_as_same_as_file_name(self) / self.source_yaml_file)
        CONFIG.load()
        yield
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


def prepare_basic_store_waon():
    """This function prepare common fixture with some tests."""
    StoreFactory(
        account=Account.WAON,
        row_data=StoreRowData('ファミリーマートかぶと町永代', 'ファミリーマート　かぶと町永代通り店'),
    )
    StoreFactory(
        account=Account.WAON,
        row_data=StoreRowData('板橋前野町', 'イオンスタイル　板橋前野町'),
    )
