"""Tests for input_csv_converter_iterator.py."""
import csv
from dataclasses import dataclass

import pytest

from tests.testlibraries.database import StoreFactory, ItemFactory
from tests.conftest import database_session_with_records
from tests.testlibraries.file import create_path_as_same_as_file_name, clean_up_directory
from zaimcsvconverter.account import Account
from zaimcsvconverter.input_csv_converter_iterator import InputCsvConverterIterator
from zaimcsvconverter.models import StoreRowData, ItemRowData


@dataclass
class ErrorRowDataForTest:
    """This class implements data class for wrapping list of error CSV row model."""
    convert_table: str
    store_name: str
    item_name: str


@pytest.fixture
def input_csv_converter_iterator(request):
    """This fixture prepares InputCsvConverterIterator."""
    path_as_same_as_file_name = create_path_as_same_as_file_name(request.function)
    directory_csv_input = path_as_same_as_file_name / request.node.name / 'csvinput'
    directory_csv_output = path_as_same_as_file_name / request.node.name / 'csvoutput'
    input_csv_converter_iterator = InputCsvConverterIterator(directory_csv_input, directory_csv_output)
    yield input_csv_converter_iterator
    clean_up_directory(directory_csv_output)


@pytest.fixture
def database_session_store_item():
    """This fixture prepares database session and records."""
    def fixture_records():
        StoreFactory(
            account=Account.WAON,
            row_data=StoreRowData('ファミリーマートかぶと町永代', 'ファミリーマート　かぶと町永代通り店'),
        )
        ItemFactory(
            account=Account.AMAZON,
            row_data=ItemRowData(
                'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト', '大型出費', '家電'
            ),
        )
    yield from database_session_with_records(fixture_records)


class TestInputCsvConverterIterator:
    """Tests for AccountCsvConverterIterator."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_success(input_csv_converter_iterator, yaml_config_load, database_session_store_item):
        """Method processes all csv files in specified diretory."""
        input_csv_converter_iterator.execute()
        files = sorted(input_csv_converter_iterator.directory_csv_output.rglob('*[!.gitkeep]'))
        assert len(files) == 2
        assert files[0].name == 'test_amazon.csv'
        assert files[1].name == 'test_waon.csv'

    # pylint: disable=unused-argument
    @staticmethod
    def test_fail(input_csv_converter_iterator, yaml_config_load, database_session_store_item):
        """
        Method exports error csv files in specified diretory.
        Same content should be unified.
        """
        with pytest.raises(KeyError):
            input_csv_converter_iterator.execute()
        files = sorted(input_csv_converter_iterator.directory_csv_output.rglob('*[!.gitkeep]'))
        assert len(files) == 3
        assert files[0].name == 'error.csv'
        assert files[1].name == 'test_amazon.csv'
        assert files[2].name == 'test_waon.csv'
        with files[0].open('r', encoding='UTF-8', newline='\n') as file_error:
            reader_error = csv.reader(file_error)
            error_row_data = ErrorRowDataForTest(*(reader_error.__next__()))
            assert error_row_data.convert_table == 'amazon.csv'
            assert error_row_data.store_name == ''
            assert error_row_data.item_name == (
                'LITTLE TREEチェアマット 120×90cm厚1.5mm 床を保護 机の擦り傷防止滑り止め カート可能 透明大型デスク足元マット フローリング/畳/床暖房対応 (120×90cm)'
            )
            error_row_data = ErrorRowDataForTest(*(reader_error.__next__()))
            assert error_row_data.convert_table == 'waon.csv'
            assert error_row_data.store_name == '板橋前野町'
            assert error_row_data.item_name == ''
