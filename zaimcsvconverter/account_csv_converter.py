#!/usr/bin/env python

"""
This module implements abstract converting steps for CSV.
"""

import csv
from pathlib import Path
from typing import NoReturn, List

import numpy

from zaimcsvconverter.account import DirectoryCsv, Account


class AccountCsvConverter:
    """
    This class implements abstract converting steps for CSV.
    """
    def __init__(self, path_csv_file: Path):
        self._path_csv_file = path_csv_file
        self._account = Account.create_by_path_csv_input(path_csv_file)
        self.list_undefined_content: List[List[str]] = []

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
            account_row_data = account_dependency.account_row_data_class(*list_row_account)
            account_row = account_dependency.account_row_factory.create(self._account, account_row_data)
            if not account_row.is_valid:
                self.list_undefined_content: List[List[str]]
                undefined_content = [account_dependency.file_name_csv_convert]
                undefined_content.extend(account_row.extract_undefined_content(account_row_data))
                self.list_undefined_content.append(undefined_content)
                continue
            if account_row.is_row_to_skip:
                continue
            zaim_row = account_row.convert_to_zaim_row()
            list_row_zaim = zaim_row.convert_to_list()
            writer_zaim.writerow(list_row_zaim)
        if self.list_undefined_content:
            self.list_undefined_content = numpy.unique(self.list_undefined_content, axis=0).tolist()
            raise KeyError(
                f'Undefined store name in convert table CSV exists in {self._path_csv_file.name}.'
                + 'Please check property AccountCsvConveter.list_undefined_store.'
            )
