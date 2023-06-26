"""This module implements config for pytest."""
from collections.abc import Generator
from pathlib import Path

from fixturefilehandler.factories import DeployerFactory
from fixturefilehandler.file_paths import YamlConfigFilePathBuilder
from fixturefilehandler import RelativeDeployFilePath, ResourceFileDeployer
import pytest
from sqlalchemy.orm.session import Session as SQLAlchemySession

from tests.test_zaim_csv_converter import create_relative_deploy_file_path
from tests.testlibraries.database_for_test import DatabaseForTest
from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter import CONFIG


@pytest.fixture()
def database_session() -> Generator[SQLAlchemySession, None, None]:
    """This fixture prepares database and fixture records."""
    yield from DatabaseForTest.database_session()


@pytest.fixture()
def database_session_with_schema(request: pytest.FixtureRequest) -> Generator[SQLAlchemySession, None, None]:
    """This fixture prepares database and fixture records."""
    yield from DatabaseForTest.database_session_with_schema(getattr(request, "param", None))


@pytest.fixture()
def database_session_basic_store_waon() -> Generator[SQLAlchemySession, None, None]:
    """This function prepare common fixture with some tests."""
    yield from DatabaseForTest.database_session_with_schema(
        [
            InstanceResource.FIXTURE_RECORD_STORE_WAON_FAMILY_MART_KABUTOCHOEITAIDORI,
            InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO,
        ],
    )


@pytest.fixture()
def database_session_stores_gold_point_card_plus() -> Generator[SQLAlchemySession, None, None]:
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema(
        [
            InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC,
            InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP,
            InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AMAZON_DOWNLOADS,
            InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AWS,
        ],
    )


@pytest.fixture()
def database_session_stores_mufg() -> Generator[SQLAlchemySession, None, None]:
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema(
        [
            InstanceResource.FIXTURE_RECORD_STORE_MUFG_EMPTY,
            InstanceResource.FIXTURE_RECORD_STORE_MUFG_MUFG,
            InstanceResource.FIXTURE_RECORD_STORE_MUFG_TOKYO_WATERWORKS,
            InstanceResource.FIXTURE_RECORD_STORE_MUFG_GOLD_POINT_MARKETING,
            InstanceResource.FIXTURE_RECORD_STORE_MUFG_OTHER_ACCOUNT,
            InstanceResource.FIXTURE_RECORD_STORE_MUFG_MUFG_TRUST_AND_BANK,
        ],
    )


@pytest.fixture()
def database_session_stores_sf_card_viewer() -> Generator[SQLAlchemySession, None, None]:
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema(
        [
            InstanceResource.FIXTURE_RECORD_STORE_PASMO_KOHRAKUEN_STATION,
            InstanceResource.FIXTURE_RECORD_STORE_PASMO_KITASENJU_STATION,
            InstanceResource.FIXTURE_RECORD_STORE_PASMO_AKIHABARA_STATION,
            InstanceResource.FIXTURE_RECORD_STORE_PASMO_EMPTY,
        ],
    )


@pytest.fixture()
def database_session_stores_view_card() -> Generator[SQLAlchemySession, None, None]:
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema(
        [InstanceResource.FIXTURE_RECORD_STORE_VIEW_CARD_VIEW_CARD],
    )


@pytest.fixture()
def database_session_store_item() -> Generator[SQLAlchemySession, None, None]:
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema(
        [
            InstanceResource.FIXTURE_RECORD_STORE_WAON_FAMILY_MART_KABUTOCHOEITAIDORI,
            InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_ECHO_DOT,
        ],
    )


@pytest.fixture()
def database_session_stores_item() -> Generator[SQLAlchemySession, None, None]:
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema(
        [
            InstanceResource.FIXTURE_RECORD_STORE_MUFG_MUFG,
            InstanceResource.FIXTURE_RECORD_STORE_PASMO_KOHRAKUEN_STATION,
            InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO,
            InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_ECHO_DOT,
        ],
    )


@pytest.fixture()
def database_session_item() -> Generator[SQLAlchemySession, None, None]:
    """This fixture prepares database session and records."""
    yield from DatabaseForTest.database_session_with_schema(
        [
            InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_ECHO_DOT,
            InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_AMAZON_POINT,
        ],
    )


@pytest.fixture()
def _yaml_config_file(resource_path_root: Path) -> Generator[None, None, None]:
    """This fixture prepares YAML config file and loads it."""
    yaml_config_file_path = YamlConfigFilePathBuilder(
        path_target_directory=InstanceResource.PATH_PROJECT_HOME_DIRECTORY,
        path_test_directory=resource_path_root,
    )
    # noinspection PyPep8Naming
    yaml_config_file_deployer = DeployerFactory.create(yaml_config_file_path)
    yaml_config_file_deployer.setup()
    yield
    yaml_config_file_deployer.teardown()


@pytest.fixture()
def _yaml_config_load(
    request: pytest.FixtureRequest,
    resource_path: Path,
    resource_path_root: Path,
) -> None:
    """This fixture prepares YAML config file and loads it."""
    CONFIG.load(get_config_file_path(request, resource_path, resource_path_root))


def get_config_file_path(request: pytest.FixtureRequest, resource_path: Path, resource_path_root: Path) -> Path:
    """This method build file path if file name is presented by parametrize."""
    if hasattr(request, "param"):
        # Reason: see: https://github.com/pytest-dev/pytest/issues/8073
        return resource_path.parent / str(request.param)
    return resource_path_root / "config.yml.dist"


@pytest.fixture()
def path_file_csv_input(request: pytest.FixtureRequest, resource_path: Path) -> Path:
    """This fixture prepare CSV output directory."""
    return get_input_csv_file_path(request, resource_path)


def get_input_csv_file_path(request: pytest.FixtureRequest, resource_path: Path) -> Path:
    """This method build file path if file name is presented by parametrize."""
    suffix = getattr(request, "param", None)
    suffix = "" if suffix is None else f"_{suffix}"
    file_name = f"{request.function.__name__}{suffix}.csv"
    return resource_path.parent / file_name


@pytest.fixture()
def directory_csv_convert_table(resource_path: Path) -> Generator[RelativeDeployFilePath, None, None]:
    """This fixture prepares directory for CSV files of convert tables."""
    csv_convert_table_file_path = create_relative_deploy_file_path(resource_path, "csvconverttable")
    ResourceFileDeployer.setup(csv_convert_table_file_path)
    yield csv_convert_table_file_path
    ResourceFileDeployer.teardown(csv_convert_table_file_path)


@pytest.fixture()
def directory_csv_input(
    request: pytest.FixtureRequest,
    resource_path: Path,
) -> Generator[RelativeDeployFilePath, None, None]:
    """This fixture prepares directory for CSV files of input."""
    csv_input_file_path = create_relative_deploy_file_path(resource_path, "csvinput", f"csvinput_{request.node.name}")
    ResourceFileDeployer.setup(csv_input_file_path)
    yield csv_input_file_path
    ResourceFileDeployer.teardown(csv_input_file_path)


@pytest.fixture()
def directory_csv_output(resource_path: Path) -> Generator[RelativeDeployFilePath, None, None]:
    """This fixture prepares directory for CSV files of output."""
    csv_output_file_path = create_relative_deploy_file_path(resource_path, "csvoutput")
    ResourceFileDeployer.setup(csv_output_file_path)
    yield csv_output_file_path
    ResourceFileDeployer.teardown(csv_output_file_path)
