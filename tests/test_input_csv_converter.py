"""Tests for input_csv_converter.py."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest
from _pytest.fixtures import FixtureRequest  # type: ignore
from fixturefilehandler import TargetFilePathVacator

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.csv_file_path_builder import CsvFilePathBuilder
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.exceptions import InvalidInputCsvError
from zaimcsvconverter.input_csv_converter import InputCsvConverter


@pytest.fixture
def path_file_csv_input_waon(request: FixtureRequest):
    """This fixture prepares csv file for WAON."""
    yield from path_file_csv_input(request, '_waon.csv')


@pytest.fixture
def path_file_csv_input_amazon(request: FixtureRequest):
    """This fixture prepares csv file for Amazon."""
    yield from path_file_csv_input(request, '_amazon.csv')


def path_file_csv_input(request: FixtureRequest, suffix_file_name: str):
    """This fixture prepare CSV output directory."""
    csv_file_path = CsvFilePathBuilder(
        target=request.node.name + suffix_file_name,
        base=InstanceResource.PATH_PROJECT_HOME_DIRECTORY
    )
    TargetFilePathVacator.setup(csv_file_path)
    yield InstanceResource.PATH_TEST_RESOURCES / Path(__file__).stem / (request.node.name + suffix_file_name)
    TargetFilePathVacator.teardown(csv_file_path)


class TestInputCsvConverterForStore:
    """Tests for AccountCsvConverter for store based CSV."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_success(path_file_csv_input_waon, yaml_config_load, database_session_basic_store_waon):
        """
        The row to skip should be skipped.
        First line should be header.
        """
        input_csv_converter = InputCsvConverter(path_file_csv_input_waon)
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == []
        input_csv_converter.execute()
        with (
                InstanceResource.PATH_PROJECT_HOME_DIRECTORY / 'csvoutput' / path_file_csv_input_waon.name
        ).open('r', encoding='UTF-8', newline='\n') as file_zaim:
            # noinspection PyUnusedLocal
            assert sum(1 for row in file_zaim) == 2
            file_zaim.seek(0)
            reader_zaim = csv.reader(file_zaim)
            list_zaim_row = reader_zaim.__next__()
            zaim_row_data = ZaimRowData(*list_zaim_row)
            assert zaim_row_data.date == '日付'
            assert zaim_row_data.method == '方法'
            assert zaim_row_data.category_large == 'カテゴリ'
            assert zaim_row_data.category_small == 'カテゴリの内訳'
            assert zaim_row_data.cash_flow_source == '支払元'
            assert zaim_row_data.cash_flow_target == '入金先'
            assert zaim_row_data.item_name == '品目'
            assert zaim_row_data.note == 'メモ'
            assert zaim_row_data.store_name == 'お店'
            assert zaim_row_data.currency == '通貨'
            assert zaim_row_data.amount_income == '収入'
            assert zaim_row_data.amount_payment == '支出'
            assert zaim_row_data.amount_transfer == '振替'
            assert zaim_row_data.balance_adjustment == '残高調整'
            assert zaim_row_data.amount_before_currency_conversion == '通貨変換前の金額'
            assert zaim_row_data.setting_aggregate == '集計の設定'

    # pylint: disable=unused-argument
    @staticmethod
    def test_stop_iteration(path_file_csv_input_waon, yaml_config_load, database_session_basic_store_waon):
        """Method should raise error when header is defined in Account Enum and CSV doesn't include header."""
        input_csv_converter = InputCsvConverter(path_file_csv_input_waon)
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == []
        with pytest.raises(InvalidInputCsvError):
            input_csv_converter.execute()

    # pylint: disable=unused-argument
    @staticmethod
    def test_key_error(path_file_csv_input_waon, yaml_config_load, database_session_basic_store_waon):
        """
        Method should raise error when store isn't be find on database.
        Undefined store is listed up on property.
        """
        input_csv_converter = InputCsvConverter(path_file_csv_input_waon)
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == []
        with pytest.raises(InvalidInputCsvError):
            input_csv_converter.execute()
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == [
            ['waon.csv', 'マクドナルド津田沼駅前店', '']
        ]


class TestInputCsvConverterForItem:
    """Tests for AcountCsvConverter for item based CSV."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_key_error(path_file_csv_input_amazon, yaml_config_load, database_session_basic_store_waon):
        """
        Method should raise error when store isn't be find on database.
        Undefined item is listed up on property.
        """
        input_csv_converter = InputCsvConverter(path_file_csv_input_amazon)
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == []
        with pytest.raises(InvalidInputCsvError):
            input_csv_converter.execute()
        assert input_csv_converter.input_csv.undefined_content_error_handler.list_error == [
            ['amazon.csv', '', 'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト']
        ]
