#!/usr/bin/env python
import csv
from abc import ABCMeta, abstractmethod
from pathlib import Path


class AccountCsvConverter(metaclass=ABCMeta):
    DIRECTORY_CSV_OUTPUT = './csvoutput/'

    def __init__(self, csv_file, encode, is_including_header):
        self._csv_file = csv_file
        self.encode = encode
        self.is_including_header = is_including_header

    def execute(self):
        with open(
            Path(self.DIRECTORY_CSV_OUTPUT) / self._csv_file.name, 'w', encoding='UTF-8', newline='\n'
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

    def _convert_from_account(self, writer_zaim):
        with open(self._csv_file, 'r', encoding=self.encode) as file_account:
            reader_account = csv.reader(file_account)
            if self.is_including_header:
                reader_account.__next__()
            self._iterate_convert(reader_account, writer_zaim)

    def _iterate_convert(self, reader_account, writer_zaim):
        for list_row_account in reader_account:
            account_row = self._create_account_row(list_row_account)
            zaim_row = account_row.convert_to_zaim_row()
            list_row_zaim = zaim_row.convert_to_list()
            writer_zaim.writerow(list_row_zaim)

    @abstractmethod
    def _create_account_row(self, list_row_account):
        pass
