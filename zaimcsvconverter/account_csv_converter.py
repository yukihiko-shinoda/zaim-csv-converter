#!/usr/bin/env python

"""
This module implements abstract converting steps for CSV.
"""

import csv
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import List, NoReturn

from zaimcsvconverter.account_row import AccountRow
from zaimcsvconverter.enum import DirectoryCsv


class AccountCsvConverter(metaclass=ABCMeta):
    """
    This class implements abstract converting steps for CSV.
    """
    def __init__(self, csv_file: Path, encode: str, is_including_header: bool):
        self._csv_file: Path = csv_file
        self.encode: str = encode
        self.is_including_header: bool = is_including_header

    def execute(self) -> NoReturn:
        """
        This method executes CSV convert steps.
        """
        with open(
                Path(DirectoryCsv.OUTPUT.value) / self._csv_file.name, 'w', encoding='UTF-8', newline='\n'
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
        with self._csv_file.open('r', encoding=self.encode) as file_account:
            reader_account = csv.reader(file_account)
            if self.is_including_header:
                reader_account.__next__()
            self._iterate_convert(reader_account, writer_zaim)

    def _iterate_convert(self, reader_account, writer_zaim) -> NoReturn:
        for list_row_account in reader_account:
            account_row = self._create_account_row(list_row_account)
            zaim_row = account_row.convert_to_zaim_row()
            list_row_zaim = zaim_row.convert_to_list()
            writer_zaim.writerow(list_row_zaim)

    @staticmethod
    @abstractmethod
    def _create_account_row(list_row_account: List[str]) -> AccountRow:
        pass
