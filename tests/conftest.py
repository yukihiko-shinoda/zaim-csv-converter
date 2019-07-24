"""This module implements config for pytest."""
from pathlib import Path

import pytest
from fixturefilehandler.factories import DeployerFactory
from fixturefilehandler.file_paths import YamlConfigFilePathBuilder

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.database_for_test import DatabaseForTest
from tests.testlibraries.file import FilePathUtility
from zaimcsvconverter import CONFIG


@pytest.fixture
def database_session():
    """This fixture prepares database and fixture records."""
    yield from DatabaseForTest.database_session()


@pytest.fixture
def database_session_with_schema(request):
    """This fixture prepares database and fixture records."""
    yield from DatabaseForTest.database_session_with_schema(getattr(request, 'param', None))


@pytest.fixture
def database_session_basic_store_waon():
    """This function prepare common fixture with some tests."""
    yield from DatabaseForTest.database_session_with_schema([
        InstanceResource.FIXTURE_RECORD_STORE_WAON_FAMILY_MART_KABUTOCHOEITAIDORI,
        InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO,
    ])


@pytest.fixture
def database_session_stores_gold_point_card_plus():
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema([
        InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC,
        InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP,
    ])


@pytest.fixture
def database_session_stores_mufg():
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema([
        InstanceResource.FIXTURE_RECORD_STORE_MUFG_EMPTY,
        InstanceResource.FIXTURE_RECORD_STORE_MUFG_MUFG,
        InstanceResource.FIXTURE_RECORD_STORE_MUFG_TOKYO_WATERWORKS,
        InstanceResource.FIXTURE_RECORD_STORE_MUFG_GOLD_POINT_MARKETING,
        InstanceResource.FIXTURE_RECORD_STORE_MUFG_OTHER_ACCOUNT,
        InstanceResource.FIXTURE_RECORD_STORE_MUFG_MUFG_TRUST_AND_BANK,
    ])


@pytest.fixture
def database_session_stores_sf_card_viewer():
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema([
        InstanceResource.FIXTURE_RECORD_STORE_PASMO_KOHRAKUEN_STATION,
        InstanceResource.FIXTURE_RECORD_STORE_PASMO_KITASENJU_STATION,
        InstanceResource.FIXTURE_RECORD_STORE_PASMO_AKIHABARA_STATION,
        InstanceResource.FIXTURE_RECORD_STORE_PASMO_EMPTY,
    ])


@pytest.fixture
def database_session_store_item():
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema([
        InstanceResource.FIXTURE_RECORD_STORE_WAON_FAMILY_MART_KABUTOCHOEITAIDORI,
        InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_ECHO_DOT,
    ])


@pytest.fixture
def database_session_stores_item():
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema([
        InstanceResource.FIXTURE_RECORD_STORE_MUFG_MUFG,
        InstanceResource.FIXTURE_RECORD_STORE_PASMO_KOHRAKUEN_STATION,
        InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO,
        InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_ECHO_DOT,
    ])


@pytest.fixture
def database_session_item():
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema([
        InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_ECHO_DOT,
    ])


YAML_CONFIG_FILE_PATH = YamlConfigFilePathBuilder(
    path_target_directory=InstanceResource.PATH_PROJECT_HOME_DIRECTORY,
    path_test_directory=Path('tests/testresources')
)
YamlConfigFileDeployer = DeployerFactory.create(YAML_CONFIG_FILE_PATH)


@pytest.fixture
def yaml_config_file():
    """This fixture prepares YAML config file and loads it."""
    YamlConfigFileDeployer.setup()
    yield
    YamlConfigFileDeployer.teardown()


@pytest.fixture
def yaml_config_load(request):
    """This fixture prepares YAML config file and loads it."""
    CONFIG.load(FilePathUtility.get_config_file_path(request))
    yield
