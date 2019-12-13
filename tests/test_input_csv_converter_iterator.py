"""Tests for input_csv_converter_iterator.py."""
import csv

import pytest

from tests.testlibraries.error_row_data_for_test import ErrorRowDataForTest
from tests.testlibraries.file import FilePathUtility
from zaimcsvconverter.exceptions import InvalidInputCsvError
from zaimcsvconverter.input_csv_converter_iterator import InputCsvConverterIterator


@pytest.fixture
def directory_csv_input(request):
    """This fixture prepares InputCsvConverterIterator."""
    yield FilePathUtility.create_path_to_resource_directory(request.function) / request.node.name


class TestInputCsvConverterIterator:
    """Tests for AccountCsvConverterIterator."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_success(yaml_config_load, database_session_store_item, directory_csv_input, tmp_path):
        """Method processes all csv files in specified diretory."""
        input_csv_converter_iterator = InputCsvConverterIterator(directory_csv_input, tmp_path)
        input_csv_converter_iterator.execute()
        files = sorted(tmp_path.rglob('*[!.gitkeep]'))
        assert len(files) == 2
        assert files[0].name == 'test_amazon.csv'
        assert files[1].name == 'test_waon.csv'

    # pylint: disable=unused-argument
    @staticmethod
    def test_fail(yaml_config_load, database_session_store_item, directory_csv_input, tmp_path):
        """
        Method exports error csv files in specified diretory.
        Same content should be unified.
        """
        input_csv_converter_iterator = InputCsvConverterIterator(directory_csv_input, tmp_path)
        with pytest.raises(InvalidInputCsvError):
            input_csv_converter_iterator.execute()
        files = sorted(tmp_path.rglob('*[!.gitkeep]'))
        assert len(files) == 4, f'files = {files}'
        assert files[0].name == 'error_invalid_row.csv'
        assert files[1].name == 'error_undefined_content.csv'
        assert files[2].name == 'test_amazon.csv'
        assert files[3].name == 'test_waon.csv'
        with files[1].open('r', encoding='UTF-8', newline='\n') as file_error:
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
