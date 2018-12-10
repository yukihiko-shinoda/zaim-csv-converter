#!/usr/bin/env python
"""Tests for account_csv_converter.py."""
from __future__ import annotations

import csv
from abc import abstractmethod
from pathlib import Path

from tests.resource import ConfigurableDatabaseTestCase, StoreFactory, CsvHandler, create_path_as_same_as_file_name
from tests.test_zaim_row import ZaimRowDataForTest
from zaimcsvconverter.account import Account
from zaimcsvconverter.account_csv_converter import AccountCsvConverter
from zaimcsvconverter.models import StoreRowData


def prepare_fixture():
    """This function prepare common fixture with some tests."""
    StoreFactory(
        account=Account.WAON,
        row_data=StoreRowData('ファミリーマートかぶと町永代', 'ファミリーマート　かぶと町永代通り店'),
    )
    StoreFactory(
        account=Account.WAON,
        row_data=StoreRowData('板橋前野町', 'イオンスタイル　板橋前野町'),
    )


class TestAccountCsvConverter(ConfigurableDatabaseTestCase):
    """Tests for AccountCsvConverter."""
    @property
    @abstractmethod
    def suffix_file_name(self):
        """This property returns suffix of file name."""
        pass

    @property
    def file_source(self) -> Path:
        """This property returns path to source file."""
        return create_path_as_same_as_file_name(self) / (self._testMethodName + self.suffix_file_name)

    def _prepare_fixture(self):
        prepare_fixture()

    def setUp(self):
        super().setUp()
        CsvHandler.set_up(self.file_source)

    def doCleanups(self):
        CsvHandler.do_cleanups(self.file_source)
        super().doCleanups()


class TestAccountCsvConverterForStore(TestAccountCsvConverter):
    """Tests for AccountCsvConverter for store based CSV."""
    @property
    def suffix_file_name(self):
        return '_waon.csv'

    def test_success(self):
        """
        The row to skip should be skipped.
        First line should be header.
        """
        account_csv_converter = AccountCsvConverter(self.file_source)
        self.assertEqual(account_csv_converter.list_undefined_content, [])
        account_csv_converter.execute()
        with open(
                str(CsvHandler.PATH_TARGET_OUTPUT / self.file_source.name), 'r', encoding='UTF-8', newline='\n'
        ) as file_zaim:
            # noinspection PyUnusedLocal
            self.assertEqual(sum(1 for row in file_zaim), 2)
            file_zaim.seek(0)
            reader_account = csv.reader(file_zaim)
            list_zaim_row = reader_account.__next__()
            zaim_row_data = ZaimRowDataForTest(*list_zaim_row)
            self.assertEqual(zaim_row_data.date, '日付')
            self.assertEqual(zaim_row_data.method, '方法')
            self.assertEqual(zaim_row_data.category_large, 'カテゴリ')
            self.assertEqual(zaim_row_data.category_small, 'カテゴリの内訳')
            self.assertEqual(zaim_row_data.cash_flow_source, '支払元')
            self.assertEqual(zaim_row_data.cash_flow_target, '入金先')
            self.assertEqual(zaim_row_data.item_name, '品目')
            self.assertEqual(zaim_row_data.note, 'メモ')
            self.assertEqual(zaim_row_data.store_name, 'お店')
            self.assertEqual(zaim_row_data.currency, '通貨')
            self.assertEqual(zaim_row_data.amount_income, '収入')
            self.assertEqual(zaim_row_data.amount_payment, '支出')
            self.assertEqual(zaim_row_data.amount_transfer, '振替')
            self.assertEqual(zaim_row_data.balance_adjustment, '残高調整')
            self.assertEqual(zaim_row_data.amount_before_currency_conversion, '通貨変換前の金額')
            self.assertEqual(zaim_row_data.setting_aggregate, '集計の設定')

    def test_stop_iteration(self):
        """Method should raise error when header is defined in Account Enum and CSV doesn't include header."""
        account_csv_converter = AccountCsvConverter(self.file_source)
        self.assertEqual(account_csv_converter.list_undefined_content, [])
        with self.assertRaises(StopIteration):
            account_csv_converter.execute()

    def test_key_error(self):
        """
        Method should raise error when store isn't be find on database.
        Undefined store is listed up on property.
        """
        account_csv_converter = AccountCsvConverter(self.file_source)
        self.assertEqual(account_csv_converter.list_undefined_content, [])
        with self.assertRaises(KeyError):
            account_csv_converter.execute()
        self.assertEqual(account_csv_converter.list_undefined_content, [['waon.csv', 'マクドナルド津田沼駅前店', '']])


class TestAccountCsvConverterForItem(TestAccountCsvConverter):
    """Tests for AcountCsvConverter for item based CSV."""
    @property
    def suffix_file_name(self):
        return '_amazon.csv'

    def test_key_error(self):
        """
        Method should raise error when store isn't be find on database.
        Undefined item is listed up on property.
        """
        account_csv_converter = AccountCsvConverter(self.file_source)
        self.assertEqual(account_csv_converter.list_undefined_content, [])
        with self.assertRaises(KeyError):
            account_csv_converter.execute()
        self.assertEqual(
            account_csv_converter.list_undefined_content,
            [['amazon.csv', '', 'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト']]
        )
