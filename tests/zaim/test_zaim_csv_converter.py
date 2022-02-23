"""Tests for zaim_csv_converter.py."""
import csv
from pathlib import Path
from typing import Optional

from fixturefilehandler.file_paths import RelativeDeployFilePath
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.integration_test_expected_factory import (
    create_zaim_row_data_amazon_201810,
    create_zaim_row_data_amazon_201911_201911,
    create_zaim_row_data_amazon_201911_202004,
    create_zaim_row_data_gold_point_card_plus_201807,
    create_zaim_row_data_gold_point_card_plus_201912_201807,
    create_zaim_row_data_mufg_201808,
    create_zaim_row_data_mufg_201810,
    create_zaim_row_data_mufg_201811,
    create_zaim_row_data_pasmo_201811,
    create_zaim_row_data_pasmo_201901,
    create_zaim_row_data_pay_pal_201810,
    create_zaim_row_data_sbi_sumishin_net_bank_202201,
    create_zaim_row_data_suica_202003,
    create_zaim_row_data_view_card_202005,
    create_zaim_row_data_waon_201807,
    create_zaim_row_data_waon_201808,
    create_zaim_row_data_waon_201810,
    create_zaim_row_data_waon_201811,
)
from tests.testlibraries.output_csv_file_checker import ErrorCsvFileChecker, ZaimCsvFileChecker
from tests.testlibraries.row_data import InvalidRowErrorRowData
from zaimcsvconverter.exceptions import InvalidInputCsvError
from zaimcsvconverter.zaim.zaim_csv_converter import ZaimCsvConverter


def create_relative_deploy_file_path(
    resource_path: Path, directory_name: str, directory_name_resource: Optional[str] = None
) -> RelativeDeployFilePath:
    """This  function creates relative path aggregate instance to deploy."""
    if directory_name_resource is None:
        directory_name_resource = directory_name
    return RelativeDeployFilePath(
        target=Path(directory_name),
        backup=Path(f"{directory_name}_bak"),
        resource=resource_path.parent / Path(directory_name_resource),
        base=InstanceResource.PATH_PROJECT_HOME_DIRECTORY,
    )


class TestZaimCsvConverter:
    """Tests for ZaimCsvConverter."""

    # pylint: disable=too-many-arguments,too-many-locals,unused-argument
    @staticmethod
    @pytest.mark.usefixtures(
        "yaml_config_file", "directory_csv_convert_table", "directory_csv_input", "database_session"
    )
    def test_success(directory_csv_output: RelativeDeployFilePath) -> None:
        """Input CSV files should be converted into Zaim format CSV file."""
        try:
            ZaimCsvConverter.execute()
        except InvalidInputCsvError as error:
            if (directory_csv_output.target / "error_undefined_content.csv").exists():
                TestZaimCsvConverter.debug_csv("error_undefined_content.csv", directory_csv_output)
            TestZaimCsvConverter.debug_csv("error_invalid_row.csv", directory_csv_output)
            raise error
        files = sorted(directory_csv_output.target.rglob("*[!.gitkeep]"))

        assert len(files) == 18
        checker = ZaimCsvFileChecker(directory_csv_output)
        checker.assert_file("waon201807.csv", create_zaim_row_data_waon_201807())
        checker.assert_file("waon201808.csv", create_zaim_row_data_waon_201808())
        checker.assert_file("waon201810.csv", create_zaim_row_data_waon_201810())
        checker.assert_file("waon201811.csv", create_zaim_row_data_waon_201811())
        checker.assert_file("gold_point_card_plus201807.csv", create_zaim_row_data_gold_point_card_plus_201807())
        checker.assert_file(
            "gold_point_card_plus_201912_202007.csv", create_zaim_row_data_gold_point_card_plus_201912_201807(),
        )
        checker.assert_file("mufg201808.csv", create_zaim_row_data_mufg_201808())
        checker.assert_file("mufg201810.csv", create_zaim_row_data_mufg_201810())
        checker.assert_file("mufg201811.csv", create_zaim_row_data_mufg_201811())
        checker.assert_file("pasmo201811.csv", create_zaim_row_data_pasmo_201811())
        checker.assert_file("pasmo201901.csv", create_zaim_row_data_pasmo_201901())
        checker.assert_file("amazon201810.csv", create_zaim_row_data_amazon_201810())
        checker.assert_file("amazon_201911_201911.csv", create_zaim_row_data_amazon_201911_201911())
        checker.assert_file("amazon_201911_202004.csv", create_zaim_row_data_amazon_201911_202004())
        checker.assert_file("view_card202005.csv", create_zaim_row_data_view_card_202005())
        checker.assert_file("suica202003.csv", create_zaim_row_data_suica_202003())
        checker.assert_file("pay_pal201810.csv", create_zaim_row_data_pay_pal_201810())
        checker.assert_file("sbi_sumishin_net_bank202201.csv", create_zaim_row_data_sbi_sumishin_net_bank_202201())

    @staticmethod
    def debug_csv(csv_file_name: str, directory_csv_output: RelativeDeployFilePath) -> None:
        with (directory_csv_output.target / csv_file_name).open("r", encoding="UTF-8", newline="\n") as file:
            csv_reader = csv.reader(file)
            for list_row_data in csv_reader:
                print(list_row_data)

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures(
        "yaml_config_file", "directory_csv_convert_table", "directory_csv_input", "database_session"
    )
    def test_fail(directory_csv_output: RelativeDeployFilePath) -> None:
        """Tests following:

        - Correct input CSV files should be converted into Zaim format CSV file.
        - Incorrect input CSV files should be reported on error_undefined_content.csv.
        """
        with pytest.raises(InvalidInputCsvError) as error:
            ZaimCsvConverter.execute()
        assert str(error.value) == "Some invalid input CSV file exists. Please check error_invalid_row.csv."
        zaim_csv_file_checker = ZaimCsvFileChecker(directory_csv_output)
        zaim_csv_file_checker.assert_file(
            "waon201808.csv", create_zaim_row_data_waon_201808(),
        )
        zaim_csv_file_checker.assert_file(
            "amazon201810.csv", create_zaim_row_data_amazon_201810(),
        )
        error_csv_file_checker = ErrorCsvFileChecker(directory_csv_output)
        error_csv_file_checker.assert_file(
            "error_invalid_row.csv",
            [
                InvalidRowErrorRowData(
                    "gold_point_card_plus_201912_202008.csv",
                    "",
                    "gold_point_card_plus_201912_202008.csv does not contain Footer row. "
                    "Confirm CSV file and footer again. "
                    "Footer = ['^$', '^$', '^$', '^$', '^$', '^\\\\d*$', '^$']",
                ),
                InvalidRowErrorRowData(
                    "mufg201810.csv",
                    "",
                    (
                        "CSV file does not contain header row.Confirm CSV file and header again. "
                        "Header = "
                        "['日付', '摘要', '摘要内容', '支払い金額', '預かり金額', '差引残高', 'メモ', '未資金化区分', '入払区分']"
                    ),
                ),
                InvalidRowErrorRowData(
                    "waon201808.csv",
                    "1",
                    'The value of "Charge kind" has not been defined in this code. Charge kind = クレジットカード',
                ),
            ],
        )
