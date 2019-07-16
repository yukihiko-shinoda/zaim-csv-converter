"""This module implements config for pytest."""
from typing import Callable

import pytest
from _pytest.fixtures import FixtureRequest  # type: ignore
from fixturefilehandler import ResourceFileDeployer
from fixturefilehandler.factories import DeployerFactory
from fixturefilehandler.file_paths import YamlConfigFilePathBuilder, SimpleDeployFilePath

from tests.testlibraries import PATH_PROJECT_HOME_DIRECTORY
from tests.testlibraries.database import create_database, StoreFactory
from tests.testlibraries.file import create_path_as_same_as_file_name
from zaimcsvconverter import Session, CONFIG
from zaimcsvconverter.account import Account
from zaimcsvconverter.models import StoreRowData


@pytest.fixture
def database_session():
    """This fixture prepares database and fixture records."""
    session = create_database()
    session.flush()
    yield session
    # Remove it, so that the next test gets a new Session()
    Session.remove()


@pytest.fixture
def database_session_basic_store_waon():
    """This function prepare common fixture with some tests."""
    def fixture_records():
        StoreFactory(
            account=Account.WAON,
            row_data=StoreRowData('ファミリーマートかぶと町永代', 'ファミリーマート　かぶと町永代通り店'),
        )
        StoreFactory(
            account=Account.WAON,
            row_data=StoreRowData('板橋前野町', 'イオンスタイル　板橋前野町'),
        )
    yield from database_session_with_records(fixture_records)


def database_session_with_records(fixture_records: Callable[[], None]):
    """This fixture prepares database and fixture records."""
    session = create_database()
    fixture_records()
    session.flush()
    yield session
    # Remove it, so that the next test gets a new Session()
    Session.remove()


YAML_CONFIG_FILE_PATH = YamlConfigFilePathBuilder(path_target_directory=PATH_PROJECT_HOME_DIRECTORY)
YamlConfigFileDeployer = DeployerFactory.create(YAML_CONFIG_FILE_PATH)


@pytest.fixture
def yaml_config():
    """This fixture prepares YAML config file and loads it."""
    YamlConfigFileDeployer.setup()
    yield
    YamlConfigFileDeployer.teardown()


@pytest.fixture
def yaml_config_load():
    """This fixture prepares YAML config file and loads it."""
    YamlConfigFileDeployer.setup()
    CONFIG.load()
    yield
    YamlConfigFileDeployer.teardown()


@pytest.fixture
def yaml_config_skip_sales_goods_row(request: FixtureRequest):
    """This fixture prepares YAML config file for test skip sales goods row."""
    yield from yaml_config_specific_source_yaml_file(request, 'config_skip_sales_goods_row.yml.dist')


@pytest.fixture
def yaml_config_not_skip_sales_goods_row(request: FixtureRequest):
    """This fixture prepares YAML config file for test not skip sales goods row."""
    yield from yaml_config_specific_source_yaml_file(request, 'config_not_skip_sales_goods_row.yml.dist')


def yaml_config_specific_source_yaml_file(request: FixtureRequest, source_yaml_file: str):
    """This fixture prepares YAML config file and loads it."""
    deploy_file_path = SimpleDeployFilePath(
        YAML_CONFIG_FILE_PATH.target,
        YAML_CONFIG_FILE_PATH.backup,
        create_path_as_same_as_file_name(request.function) / source_yaml_file
    )
    ResourceFileDeployer.setup(deploy_file_path)
    CONFIG.load()
    yield
    ResourceFileDeployer.teardown(deploy_file_path)
