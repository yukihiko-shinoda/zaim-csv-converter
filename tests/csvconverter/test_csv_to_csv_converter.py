"""Tests for input_csv_converter.py."""

from __future__ import annotations

import csv
from typing import TYPE_CHECKING

import pytest

from tests.testlibraries.assert_list import assert_each_properties
from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.csvconverter.csv_to_csv_converter import CsvToCsvConverter
from zaimcsvconverter.exceptions.invalid_input_csv_error import InvalidInputCsvError

if TYPE_CHECKING:
    from pathlib import Path


class TestCsvToCsvConverterForStore:
    """Tests for AccountCsvConverter for store based CSV."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize("path_file_csv_input", ["waon"], indirect=["path_file_csv_input"])
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_basic_store_waon")
    def test_success(path_file_csv_input: Path, tmp_path: Path) -> None:
        """Tests following:

        - The row to skip should be skipped.
        - First line should be header.
        """
        expected_length = 2
        csv_to_csv_converter = CsvToCsvConverter(path_file_csv_input, tmp_path)
        assert csv_to_csv_converter.convert_workflow.data_source.undefined_content_error_handler.list_error == []
        csv_to_csv_converter.execute()
        with (tmp_path / path_file_csv_input.name).open("r", encoding="UTF-8", newline="\n") as file_zaim:
            # noinspection PyUnusedLocal
            assert sum(1 for row in file_zaim) == expected_length
            file_zaim.seek(0)
            reader_zaim = csv.reader(file_zaim)
            list_zaim_row = next(reader_zaim)
            zaim_row_data = ZaimRowData(*list_zaim_row)
            assert_each_properties(
                zaim_row_data,
                # Reason: Duplicate with production code. pylint: disable=duplicate-code
                [
                    "日付",
                    "方法",
                    "カテゴリ",
                    "カテゴリの内訳",
                    "支払元",
                    "入金先",
                    "品目",
                    "メモ",
                    "お店",
                    "通貨",
                    "収入",
                    "支出",
                    "振替",
                    "残高調整",
                    "通貨変換前の金額",
                    "集計の設定",
                ],
            )

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize("path_file_csv_input", ["waon"], indirect=["path_file_csv_input"])
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_basic_store_waon")
    def test_stop_iteration_header(path_file_csv_input: Path, tmp_path: Path) -> None:
        """Method should raise error when header is defined in Account Enum and CSV doesn't include header."""
        input_csv_converter = CsvToCsvConverter(path_file_csv_input, tmp_path)
        assert input_csv_converter.convert_workflow.data_source.undefined_content_error_handler.list_error == []
        with pytest.raises(InvalidInputCsvError):
            input_csv_converter.execute()

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize("path_file_csv_input", ["gold_point_card_plus_201912"], indirect=["path_file_csv_input"])
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_gold_point_card_plus")
    def test_stop_iteration_footer(path_file_csv_input: Path, tmp_path: Path) -> None:
        """Method should raise error when header is defined in Account Enum and CSV doesn't include header."""
        input_csv_converter = CsvToCsvConverter(path_file_csv_input, tmp_path)
        assert input_csv_converter.convert_workflow.data_source.undefined_content_error_handler.list_error == []
        with pytest.raises(InvalidInputCsvError):
            input_csv_converter.execute()

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema",
        [[InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO]],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.parametrize("path_file_csv_input", ["waon"], indirect=["path_file_csv_input"])
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_with_schema")
    def test_key_error(path_file_csv_input: Path, tmp_path: Path) -> None:
        """Tests following:

        - Method should raise error when store isn't be find on database.
        - Undefined store is listed up on property.
        """
        input_csv_converter = CsvToCsvConverter(path_file_csv_input, tmp_path)
        assert input_csv_converter.convert_workflow.data_source.undefined_content_error_handler.list_error == []
        with pytest.raises(InvalidInputCsvError):
            input_csv_converter.execute()
        assert input_csv_converter.convert_workflow.data_source.undefined_content_error_handler.list_error == [
            ["waon.csv", "マクドナルド津田沼駅前店", ""],
        ]


class TestInputCsvConverterForItem:
    """Tests for AcountCsvConverter for item based CSV."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize("path_file_csv_input", ["amazon"], indirect=["path_file_csv_input"])
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_with_schema")
    def test_key_error(path_file_csv_input: Path, tmp_path: Path) -> None:
        """Tests following:

        - Method should raise error when store isn't be find on database.
        - Undefined item is listed up on property.
        """
        input_csv_converter = CsvToCsvConverter(path_file_csv_input, tmp_path)
        assert input_csv_converter.convert_workflow.data_source.undefined_content_error_handler.list_error == []
        with pytest.raises(InvalidInputCsvError):
            input_csv_converter.execute()
        assert input_csv_converter.convert_workflow.data_source.undefined_content_error_handler.list_error == [
            ["amazon.csv", "", "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト"],
        ]
