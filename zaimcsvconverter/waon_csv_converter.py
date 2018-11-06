#!/usr/bin/env python
import csv

from zaimcsvconverter.session_manager import SessionManager
from zaimcsvconverter.models import WaonStore, initialize_database
from zaimcsvconverter.waon.waon_row_factory import WaonRowFactory


class WaonCsvConverter(object):
    CSV_FILE_ZAIM = './csvoutput/zaim.csv'
    CSV_FILE_CONVERT_WAON_ZAIM = './csvconverttable/waon-zaim.csv'

    def __init__(self, csv_file_waon):
        initialize_database()
        self._csv_file_waon = csv_file_waon

    def execute(self):
        with SessionManager() as session_manager:
            self._import_waon_store_to_database(session_manager)
            self._convert(session_manager)

    def _import_waon_store_to_database(self, session_wrapper):
        with open(self.CSV_FILE_CONVERT_WAON_ZAIM, 'r', encoding='UTF-8') as file_convert_waon_zaim:
            reader_convert_waon_zaim = csv.reader(file_convert_waon_zaim)
            for list_row_convert_waon_zaim in reader_convert_waon_zaim:
                waon_store = WaonStore(*list_row_convert_waon_zaim)
                session_wrapper.save_waon_store(waon_store)

    def _convert(self, database_wrapper):
        with open(self.CSV_FILE_ZAIM, 'w', encoding='UTF-8', newline='\n') as file_zaim:
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
            self._convert_from_waon(database_wrapper, writer_zaim)

    def _convert_from_waon(self, database_wrapper, writer_zaim):
        with open(self._csv_file_waon, 'r', encoding='UTF-8') as file_waon:
            reader_waon = csv.reader(file_waon)
            reader_waon.__next__()
            for list_row_waon in reader_waon:
                waon_row = WaonRowFactory.create(list_row_waon)
                zaim_row = waon_row.convert_to_zaim_row(database_wrapper)
                list_row_zaim = zaim_row.convert_to_list()
                writer_zaim.writerow(list_row_zaim)
