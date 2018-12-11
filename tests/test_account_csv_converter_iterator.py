#!/usr/bin/env python
"""Tests for account_csv_converter_iterator.py."""
import csv
from dataclasses import dataclass

from tests.resource import DatabaseTestCase, create_path_as_same_as_file_name, StoreFactory, clean_up_directory, \
    ItemFactory
from zaimcsvconverter.account import Account
from zaimcsvconverter.account_csv_converter_iterator import AccountCsvConverterIterator
from zaimcsvconverter.models import StoreRowData, ItemRowData


@dataclass
class ErrorRowDataForTest:
    """This class implements data class for wrapping list of error CSV row model."""
    convert_table: str
    store_name: str
    item_name: str


class TestAccountCsvConverterIterator(DatabaseTestCase):
    """Tests for AccountCsvConverterIterator."""
    account_csv_converter = None
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

    def setUp(self):
        super().setUp()
        self.directory_csv_input = create_path_as_same_as_file_name(self) / self._testMethodName / 'csvinput'
        self.directory_csv_output = create_path_as_same_as_file_name(self) / self._testMethodName / 'csvoutput'
        self.account_csv_converter = AccountCsvConverterIterator(self.directory_csv_input, self.directory_csv_output)

    def doCleanups(self):
        clean_up_directory(self.directory_csv_output)
        super().doCleanups()

    def test_success(self):
        """Method processes all csv files in specified diretory."""
        self.account_csv_converter.execute()
        files = sorted(self.directory_csv_output.rglob('*[!.gitkeep]'))
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].name, 'test_amazon.csv')
        self.assertEqual(files[1].name, 'test_waon.csv')

    def test_fail(self):
        """
        Method exports error csv files in specified diretory.
        Same content should be unified.
        """
        with self.assertRaises(KeyError):
            self.account_csv_converter.execute()
        files = sorted(self.directory_csv_output.rglob('*[!.gitkeep]'))
        self.assertEqual(len(files), 3)
        self.assertEqual(files[0].name, 'error.csv')
        self.assertEqual(files[1].name, 'test_amazon.csv')
        self.assertEqual(files[2].name, 'test_waon.csv')
        with files[0].open('r', encoding='UTF-8', newline='\n') as file_error:
            reader_error = csv.reader(file_error)
            error_row_data = ErrorRowDataForTest(*(reader_error.__next__()))
            self.assertEqual(error_row_data.convert_table, 'amazon.csv')
            self.assertEqual(error_row_data.store_name, '')
            self.assertEqual(
                error_row_data.item_name,
                'LITTLE TREEチェアマット 120×90cm厚1.5mm 床を保護 机の擦り傷防止滑り止め カート可能 透明大型デスク足元マット フローリング/畳/床暖房対応 (120×90cm)'
            )
            error_row_data = ErrorRowDataForTest(*(reader_error.__next__()))
            self.assertEqual(error_row_data.convert_table, 'waon.csv')
            self.assertEqual(error_row_data.store_name, '板橋前野町')
            self.assertEqual(error_row_data.item_name, '')
