"""Tests for input_csv_converter.py."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.csvconverter.input_csv_converter import InputCsvConverter
from zaimcsvconverter.exceptions import InvalidInputCsvError


class TestInputCsvConverterForStore:
    """Tests for AccountCsvConverter for store based CSV."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize("path_file_csv_input", ("waon",), indirect=["path_file_csv_input"])
    @pytest.mark.usefixtures("yaml_config_load", "database_session_basic_store_waon")
    def test_success(path_file_csv_input: Path, tmp_path: Path) -> None:
        """Tests following:

        - The row to skip should be skipped.
        - First line should be header.
        """
        input_csv_converter = InputCsvConverter(path_file_csv_input, tmp_path)
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == []
        input_csv_converter.execute()
        with (tmp_path / path_file_csv_input.name).open("r", encoding="UTF-8", newline="\n") as file_zaim:
            # noinspection PyUnusedLocal
            assert sum(1 for row in file_zaim) == 2
            file_zaim.seek(0)
            reader_zaim = csv.reader(file_zaim)
            list_zaim_row = reader_zaim.__next__()
            zaim_row_data = ZaimRowData(*list_zaim_row)
            assert zaim_row_data.date == "日付"
            assert zaim_row_data.method == "方法"
            assert zaim_row_data.category_large == "カテゴリ"
            assert zaim_row_data.category_small == "カテゴリの内訳"
            assert zaim_row_data.cash_flow_source == "支払元"
            assert zaim_row_data.cash_flow_target == "入金先"
            assert zaim_row_data.item_name == "品目"
            assert zaim_row_data.note == "メモ"
            assert zaim_row_data.store_name == "お店"
            assert zaim_row_data.currency == "通貨"
            assert zaim_row_data.amount_income == "収入"
            assert zaim_row_data.amount_payment == "支出"
            assert zaim_row_data.amount_transfer == "振替"
            assert zaim_row_data.balance_adjustment == "残高調整"
            assert zaim_row_data.amount_before_currency_conversion == "通貨変換前の金額"
            assert zaim_row_data.setting_aggregate == "集計の設定"

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize("path_file_csv_input", ("waon",), indirect=["path_file_csv_input"])
    @pytest.mark.usefixtures("yaml_config_load", "database_session_basic_store_waon")
    def test_stop_iteration_header(path_file_csv_input: Path, tmp_path: Path) -> None:
        """Method should raise error when header is defined in Account Enum and CSV doesn't include header."""
        input_csv_converter = InputCsvConverter(path_file_csv_input, tmp_path)
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == []
        with pytest.raises(InvalidInputCsvError):
            input_csv_converter.execute()

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize("path_file_csv_input", ("gold_point_card_plus_201912",), indirect=["path_file_csv_input"])
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_gold_point_card_plus")
    def test_stop_iteration_footer(path_file_csv_input: Path, tmp_path: Path) -> None:
        """Method should raise error when header is defined in Account Enum and CSV doesn't include header."""
        input_csv_converter = InputCsvConverter(path_file_csv_input, tmp_path)
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == []
        with pytest.raises(InvalidInputCsvError):
            input_csv_converter.execute()

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema",
        [[InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO]],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.parametrize("path_file_csv_input", ("waon",), indirect=["path_file_csv_input"])
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test_key_error(path_file_csv_input: Path, tmp_path: Path) -> None:
        """Tests following:

        - Method should raise error when store isn't be find on database.
        - Undefined store is listed up on property.
        """
        input_csv_converter = InputCsvConverter(path_file_csv_input, tmp_path)
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == []
        with pytest.raises(InvalidInputCsvError):
            input_csv_converter.execute()
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == [
            ["waon.csv", "マクドナルド津田沼駅前店", ""]
        ]


class TestInputCsvConverterForItem:
    """Tests for AcountCsvConverter for item based CSV."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize("path_file_csv_input", ("amazon",), indirect=["path_file_csv_input"])
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test_key_error(path_file_csv_input: Path, tmp_path: Path) -> None:
        """Tests following:

        - Method should raise error when store isn't be find on database.
        - Undefined item is listed up on property.
        """
        input_csv_converter = InputCsvConverter(path_file_csv_input, tmp_path)
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == []
        with pytest.raises(InvalidInputCsvError):
            input_csv_converter.execute()
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == [
            ["amazon.csv", "", "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト"]
        ]
