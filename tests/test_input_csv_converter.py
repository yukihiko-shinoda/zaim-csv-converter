#!/usr/bin/env python
"""Tests for input_csv_converter.py."""
from __future__ import annotations

import csv
from abc import abstractmethod
from pathlib import Path

import pytest

from tests.resource import ConfigurableDatabaseTestCase, CsvHandler, create_path_as_same_as_file_name, \
    prepare_basic_store_waon
from tests.test_zaim_row import ZaimRowDataForTest
from zaimcsvconverter import CONFIG
from zaimcsvconverter.input_csv_converter import InputCsvConverter


def prepare_fixture():
    """This function prepare common fixture with some tests."""
    prepare_basic_store_waon()


class TestInputCsvConverter(ConfigurableDatabaseTestCase):
    """Tests for AccountCsvConverter."""
    method_name: str = None
    @property
    @abstractmethod
    def suffix_file_name(self):
        """This property returns suffix of file name."""

    @property
    def file_source(self) -> Path:
        """This property returns path to source file."""
        return create_path_as_same_as_file_name(self) / (self.method_name + self.suffix_file_name)

    def _prepare_fixture(self):
        prepare_fixture()

    @pytest.fixture(autouse=True)
    def csv_output_directory(self, request):
        """This fixture prepare CSV output directory."""
        self.method_name = request.node.name
        CsvHandler.set_up(self.file_source)
        CONFIG.load()
        yield
        CsvHandler.do_cleanups(self.file_source)


class TestInputCsvConverterForStore(TestInputCsvConverter):
    """Tests for AccountCsvConverter for store based CSV."""
    @property
    def suffix_file_name(self):
        return '_waon.csv'

    def test_success(self):
        """
        The row to skip should be skipped.
        First line should be header.
        """
        input_csv_converter = InputCsvConverter(self.file_source)
        assert input_csv_converter.error_handler.list_error == []
        input_csv_converter.execute()
        with open(
                str(CsvHandler.PATH_TARGET_OUTPUT / self.file_source.name), 'r', encoding='UTF-8', newline='\n'
        ) as file_zaim:
            # noinspection PyUnusedLocal
            assert sum(1 for row in file_zaim) == 2
            file_zaim.seek(0)
            reader_zaim = csv.reader(file_zaim)
            list_zaim_row = reader_zaim.__next__()
            zaim_row_data = ZaimRowDataForTest(*list_zaim_row)
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

    def test_stop_iteration(self):
        """Method should raise error when header is defined in Account Enum and CSV doesn't include header."""
        input_csv_converter = InputCsvConverter(self.file_source)
        assert input_csv_converter.error_handler.list_error == []
        with pytest.raises(StopIteration):
            input_csv_converter.execute()

    def test_key_error(self):
        """
        Method should raise error when store isn't be find on database.
        Undefined store is listed up on property.
        """
        input_csv_converter = InputCsvConverter(self.file_source)
        assert input_csv_converter.error_handler.list_error == []
        with pytest.raises(KeyError):
            input_csv_converter.execute()
        assert input_csv_converter.error_handler.list_error == [['waon.csv', 'マクドナルド津田沼駅前店', '']]


class TestInputCsvConverterForItem(TestInputCsvConverter):
    """Tests for AcountCsvConverter for item based CSV."""
    @property
    def suffix_file_name(self):
        return '_amazon.csv'

    def test_key_error(self):
        """
        Method should raise error when store isn't be find on database.
        Undefined item is listed up on property.
        """
        input_csv_converter = InputCsvConverter(self.file_source)
        assert input_csv_converter.error_handler.list_error == []
        with pytest.raises(KeyError):
            input_csv_converter.execute()
        assert input_csv_converter.error_handler.list_error == [
            ['amazon.csv', '', 'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト']
        ]
