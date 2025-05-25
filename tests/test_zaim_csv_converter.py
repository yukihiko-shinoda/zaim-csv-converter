"""Tests for zaim_csv_converter.py."""

import csv
from logging import getLogger
from pathlib import Path
from typing import Optional

import pytest
from fixturefilehandler.file_paths import RelativeDeployFilePath

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_amazon_201810
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_amazon_201911_201911
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_amazon_201911_202004
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_amazon_201911_202006
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_amazon_201911_202012
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_gold_point_card_plus_201807
from tests.testlibraries.integration_test_expected_factory import (
    create_zaim_row_data_gold_point_card_plus_201912_201807,  # noqa: H301,RUF100
)
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_mobile_suica_202210
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_mobile_suica_202211
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_mobile_suica_202212
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_mobile_suica_202301
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_mufg_201808
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_mufg_201810
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_mufg_201811
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_mufg_202304
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_pasmo_201811
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_pasmo_201901
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_pay_pal_201810
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_pay_pay_card_202208
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_sbi_sumishin_net_bank_202201
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_suica_202003
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_view_card_202005
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_waon_201807
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_waon_201808
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_waon_201810
from tests.testlibraries.integration_test_expected_factory import create_zaim_row_data_waon_201811
from tests.testlibraries.output_csv_file_checker import ErrorCsvFileChecker
from tests.testlibraries.output_csv_file_checker import ZaimCsvFileChecker
from tests.testlibraries.row_data import InvalidRowErrorRowData
from zaimcsvconverter.exceptions import SomeInvalidInputCsvError
from zaimcsvconverter.zaim_csv_converter import ZaimCsvConverter


def create_relative_deploy_file_path(
    resource_path: Path,
    directory_name: str,
    directory_name_resource: Optional[str] = None,
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
        "_yaml_config_file",
        "directory_csv_convert_table",
        "directory_csv_input",
        "database_session",
    )
    def test_success(directory_csv_output: RelativeDeployFilePath) -> None:
        """Input CSV files should be converted into Zaim format CSV file."""
        try:
            ZaimCsvConverter.execute()
        except SomeInvalidInputCsvError:
            if (directory_csv_output.target / "error_undefined_content.csv").exists():
                TestZaimCsvConverter.debug_csv("error_undefined_content.csv", directory_csv_output)
            TestZaimCsvConverter.debug_csv("error_invalid_row.csv", directory_csv_output)
            raise
        files = sorted(directory_csv_output.target.rglob("*[!.gitkeep]"))
        expected_length = 26
        assert len(files) == expected_length, ",\n".join(str(file) for file in files)
        checker = ZaimCsvFileChecker(directory_csv_output)
        checker.assert_file("waon201807.csv", create_zaim_row_data_waon_201807())
        checker.assert_file("waon201808.csv", create_zaim_row_data_waon_201808())
        checker.assert_file("waon201810.csv", create_zaim_row_data_waon_201810())
        checker.assert_file("waon201811.csv", create_zaim_row_data_waon_201811())
        checker.assert_file("gold_point_card_plus201807.csv", create_zaim_row_data_gold_point_card_plus_201807())
        checker.assert_file(
            "gold_point_card_plus_201912_202007.csv",
            create_zaim_row_data_gold_point_card_plus_201912_201807(),
        )
        checker.assert_file("mufg201808.csv", create_zaim_row_data_mufg_201808())
        checker.assert_file("mufg201810.csv", create_zaim_row_data_mufg_201810())
        checker.assert_file("mufg201811.csv", create_zaim_row_data_mufg_201811())
        checker.assert_file("mufg202304.csv", create_zaim_row_data_mufg_202304())
        checker.assert_file("pasmo201811.csv", create_zaim_row_data_pasmo_201811())
        checker.assert_file("pasmo201901.csv", create_zaim_row_data_pasmo_201901())
        checker.assert_file("amazon201810.csv", create_zaim_row_data_amazon_201810())
        checker.assert_file("amazon_201911_201911.csv", create_zaim_row_data_amazon_201911_201911())
        checker.assert_file("amazon_201911_202004.csv", create_zaim_row_data_amazon_201911_202004())
        checker.assert_file("amazon_201911_202006.csv", create_zaim_row_data_amazon_201911_202006())
        checker.assert_file("amazon_201911_202012.csv", create_zaim_row_data_amazon_201911_202012())
        checker.assert_file("view_card202005.csv", create_zaim_row_data_view_card_202005())
        checker.assert_file("suica202003.csv", create_zaim_row_data_suica_202003())
        checker.assert_file("pay_pal201810.csv", create_zaim_row_data_pay_pal_201810())
        checker.assert_file("sbi_sumishin_net_bank202201.csv", create_zaim_row_data_sbi_sumishin_net_bank_202201())
        checker.assert_file("pay_pay_card_202208.csv", create_zaim_row_data_pay_pay_card_202208())
        checker.assert_file("mobile_suica_202210.csv", create_zaim_row_data_mobile_suica_202210())
        checker.assert_file("mobile_suica_202211.csv", create_zaim_row_data_mobile_suica_202211())
        checker.assert_file("mobile_suica_202212.csv", create_zaim_row_data_mobile_suica_202212())
        checker.assert_file("mobile_suica_202301.csv", create_zaim_row_data_mobile_suica_202301())

    @staticmethod
    def debug_csv(csv_file_name: str, directory_csv_output: RelativeDeployFilePath) -> None:
        logger = getLogger(__name__)
        with (directory_csv_output.target / csv_file_name).open("r", encoding="UTF-8", newline="\n") as file:
            csv_reader = csv.reader(file)
            for list_row_data in csv_reader:
                logger.info(list_row_data)

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures(
        "_yaml_config_file",
        "directory_csv_convert_table",
        "directory_csv_input",
        "database_session",
    )
    def test_fail(directory_csv_output: RelativeDeployFilePath) -> None:
        """Tests following:

        - Correct input CSV files should be converted into Zaim format CSV file.
        - Incorrect input CSV files should be reported on error_undefined_content.csv.
        """
        with pytest.raises(SomeInvalidInputCsvError) as error:
            ZaimCsvConverter.execute()
        assert str(error.value) == "Some invalid input CSV file exists. Please check error_invalid_row.csv."
        zaim_csv_file_checker = ZaimCsvFileChecker(directory_csv_output)
        zaim_csv_file_checker.assert_file(
            "waon201808.csv",
            create_zaim_row_data_waon_201808(),
        )
        zaim_csv_file_checker.assert_file(
            "amazon201810.csv",
            create_zaim_row_data_amazon_201810(),
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
                        "['日付', '摘要', '摘要内容', '支払い金額', '預かり金額', "
                        "'差引残高', 'メモ', '未資金化区分', '入払区分']"
                    ),
                ),
                InvalidRowErrorRowData(
                    "waon201808.csv",
                    "1",
                    "Invalid 4, Input should be '銀行口座', 'ポイント', '現金', 'バリューダウンロード' or '-'",
                ),
            ],
        )
