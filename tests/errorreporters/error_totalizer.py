"""Tests for input_csv_converter_iterator.py."""
import csv
from pathlib import Path

import pytest

from tests.testlibraries.assert_list import assert_each_properties
from tests.testlibraries.error_row_data_for_test import ErrorRowDataForTest
from zaimcsvconverter.errorreporters.error_totalizer import ErrorTotalizer


class TestErrorTotalizer:
    """Tests for AccountCsvConverterIterator."""

    # pylint: disable=unused-argument
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_store_item")
    def test_success(self, resource_path: Path, tmp_path: Path) -> None:
        """Method processes all csv files in specified diretory."""
        list_expected_file = ["test_amazon.csv", "test_waon.csv"]
        error_totalizer = ErrorTotalizer(tmp_path)
        for path_csv_file in sorted(resource_path.glob("*.csv")):
            error_totalizer.convert_csv(path_csv_file)
        assert not error_totalizer.is_presented
        self.assert_files(tmp_path, list_expected_file)

    def assert_files(self, tmp_path: Path, list_expected_file: list[str]) -> None:
        files = sorted(tmp_path.rglob("*[!.gitkeep]"))
        assert len(files) == len(list_expected_file)
        for actual, expected in zip(files, list_expected_file):
            assert actual.name == expected

    # pylint: disable=unused-argument
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_store_item")
    def test_fail(self, resource_path: Path, tmp_path: Path) -> None:
        """Tests following:

        - Method exports error csv files in specified directory.
        - Same content should be unified.
        """
        list_expected_file = ["error_amazon.csv", "error_waon.csv", "test_amazon.csv", "test_waon.csv"]
        error_totalizer = ErrorTotalizer(tmp_path)
        for path_csv_file in sorted(resource_path.glob("*.csv")):
            error_totalizer.convert_csv(path_csv_file)
        assert error_totalizer.is_presented
        error_totalizer.report_to_csv()
        self.assert_files(tmp_path, list_expected_file)
        self.assert_error_csv(tmp_path)

    def assert_error_csv(self, tmp_path: Path) -> None:
        """Asserts error csv file."""
        files = sorted(tmp_path.rglob("*[!.gitkeep]"))
        with files[1].open("r", encoding="UTF-8", newline="\n") as file_error:
            reader_error = csv.reader(file_error)
            expected_item_name = "".join(
                [
                    "LITTLE TREEチェアマット 120×90cm厚1.5mm 床を保護 机の擦り傷防止滑り止め ",  # noqa: RUF001
                    "カート可能 透明大型デスク足元マット フローリング/畳/床暖房対応 (120×90cm)",  # noqa: RUF001
                ],
            )
            error_row_data = ErrorRowDataForTest(*(next(reader_error)))
            assert_each_properties(error_row_data, ["amazon.csv", None, expected_item_name])
            error_row_data = ErrorRowDataForTest(*(next(reader_error)))
            assert_each_properties(error_row_data, ["waon.csv", "板橋前野町", None])
