#!/usr/bin/env python
"""Tests for input_csv_converter_iterator.py."""
import csv
from dataclasses import dataclass

import pytest

from tests.resource import DatabaseTestCase, create_path_as_same_as_file_name, StoreFactory, clean_up_directory, \
    ItemFactory, ConfigurableDatabaseTestCase
from zaimcsvconverter.account import Account
from zaimcsvconverter.input_csv_converter_iterator import InputCsvConverterIterator
from zaimcsvconverter.models import StoreRowData, ItemRowData


@dataclass
class ErrorRowDataForTest:
    """This class implements data class for wrapping list of error CSV row model."""
    convert_table: str
    store_name: str
    item_name: str


class TestInputCsvConverterIterator(ConfigurableDatabaseTestCase):
    """Tests for AccountCsvConverterIterator."""
    input_csv_converter = None
    directory_csv_input = None
    directory_csv_output = None

    def _prepare_fixture(self):
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

    @pytest.fixture(autouse=True)
    def input_csv_converter_iterator(self, request):
        self.directory_csv_input = create_path_as_same_as_file_name(self) / request.node.name / 'csvinput'
        self.directory_csv_output = create_path_as_same_as_file_name(self) / request.node.name / 'csvoutput'
        self.input_csv_converter = InputCsvConverterIterator(self.directory_csv_input, self.directory_csv_output)
        yield
        clean_up_directory(self.directory_csv_output)

    def test_success(self):
        """Method processes all csv files in specified diretory."""
        self.input_csv_converter.execute()
        files = sorted(self.directory_csv_output.rglob('*[!.gitkeep]'))
        assert len(files) == 2
        assert files[0].name == 'test_amazon.csv'
        assert files[1].name == 'test_waon.csv'

    def test_fail(self):
        """
        Method exports error csv files in specified diretory.
        Same content should be unified.
        """
        with pytest.raises(KeyError):
            self.input_csv_converter.execute()
        files = sorted(self.directory_csv_output.rglob('*[!.gitkeep]'))
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
