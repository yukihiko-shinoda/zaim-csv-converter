#!/usr/bin/env python

"""
This module implements abstract converting steps for CSV.
"""

import csv
from pathlib import Path
from typing import NoReturn

from zaimcsvconverter.enum import DirectoryCsv, AccountDependency


class AccountCsvConverter:
    """
    This class implements abstract converting steps for CSV.
    """
    def __init__(self, path_csv_file: Path, account_dependency: AccountDependency):
        self._path_csv_file = path_csv_file
        self._account_dependency = account_dependency

    def execute(self) -> NoReturn:
        """
        This method executes CSV convert steps.
        """
        with open(
                Path(DirectoryCsv.OUTPUT.value) / self._path_csv_file.name, 'w', encoding='UTF-8', newline='\n'
        ) as file_zaim:
            writer_zaim = csv.writer(file_zaim)
            writer_zaim.writerow([
                '日付',
                '方法',
                'カテゴリ',
                'カテゴリの内訳',
                '支払元',
                '入金先',
                '品名',
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
        with self._path_csv_file.open('r', encoding=self._account_dependency.encode) as file_account:
            reader_account = csv.reader(file_account)
            if self._account_dependency.is_including_header:
                reader_account.__next__()
            self._iterate_convert(reader_account, writer_zaim)

    def _iterate_convert(self, reader_account, writer_zaim) -> NoReturn:
        for list_row_account in reader_account:
            account_row_data = self._account_dependency.account_row_data_class(*list_row_account)
            account_row = self._account_dependency.account_row_class.create(account_row_data)
            zaim_row = account_row.convert_to_zaim_row()
            list_row_zaim = zaim_row.convert_to_list()
            writer_zaim.writerow(list_row_zaim)
