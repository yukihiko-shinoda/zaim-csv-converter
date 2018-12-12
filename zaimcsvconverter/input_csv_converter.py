#!/usr/bin/env python
"""This module implements abstract converting steps for CSV."""
import csv
from pathlib import Path
from typing import NoReturn

from zaimcsvconverter.account import DirectoryCsv, Account
from zaimcsvconverter.error_handler import ErrorHandler


class InputCsvConverter:
    """This class implements abstract converting steps for CSV."""
    def __init__(self, path_csv_file: Path, directory_csv_output: Path = DirectoryCsv.OUTPUT.value):
        self._path_csv_file = path_csv_file
        self.directory_csv_output = directory_csv_output
        self._account = Account.create_by_path_csv_input(path_csv_file)
        self.error_handler: ErrorHandler = ErrorHandler()

    def execute(self) -> NoReturn:
        """This method executes CSV convert steps."""
        with (self.directory_csv_output / self._path_csv_file.name).open(
                'w', encoding='UTF-8', newline='\n'
        ) as file_zaim:
            writer_zaim = csv.writer(file_zaim)
            writer_zaim.writerow([
                '日付',
                '方法',
                'カテゴリ',
                'カテゴリの内訳',
                '支払元',
                '入金先',
                '品目',
                'メモ',
                'お店',
                '通貨',
                '収入',
                '支出',
                '振替',
                '残高調整',
                '通貨変換前の金額',
                '集計の設定'
            ])
            self._convert_from_account(writer_zaim)

    def _convert_from_account(self, writer_zaim) -> NoReturn:
        account_dependency = self._account.value
        with self._path_csv_file.open('r', encoding=account_dependency.encode) as file_account:
            reader_account = csv.reader(file_account)
            if account_dependency.csv_header:
                try:
                    while reader_account.__next__() != account_dependency.csv_header:
                        pass
                except StopIteration as error:
                    raise StopIteration(
                        f'{self._path_csv_file.name} doesn\'t include header row.'
                        + 'Please confirm AccountConfig.csv_header. '
                        + f'AccountConfig.csv_header = {account_dependency.csv_header}'
                    ) from error
            self._iterate_convert(reader_account, writer_zaim)

    def _iterate_convert(self, reader_account, writer_zaim) -> NoReturn:
        for list_row_account in reader_account:
            account_dependency = self._account.value
            input_row_data = account_dependency.input_row_data_class(*list_row_account)
            input_row = account_dependency.input_row_factory.create(self._account, input_row_data)
            if not input_row.is_valid:
                self.error_handler.append_undefined_content(self._account, input_row_data)
                continue
            if input_row.is_row_to_skip:
                continue
            zaim_row = input_row.convert_to_zaim_row()
            list_row_zaim = zaim_row.convert_to_list()
            writer_zaim.writerow(list_row_zaim)
        if self.error_handler.is_presented:
            self.error_handler.uniquify()
            raise KeyError(
                f'Undefined store name in convert table CSV exists in {self._path_csv_file.name}.'
                + 'Please check property AccountCsvConveter.list_undefined_store.'
            )
