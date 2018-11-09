#!/usr/bin/env python
import csv
import re
from pathlib import Path

from zaimcsvconverter import CONFIG
from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_csv_converter import GoldPointCardPlusCsvConverter
from zaimcsvconverter.models import initialize_database, Store
from zaimcsvconverter.session_manager import SessionManager


class ZaimCsvConverter(object):
    DIRECTORY_CSV_CONVERT = './csvconverttable/'
    DIRECTORY_CSV_INPUT = './csvinput/'
    FILE_CSV_CONVERT_WAON = 'waon.csv'
    FILE_CSV_CONVERT_GOLD_POINT_CARD_PLUS = 'gold_point_card_plus.csv'

    def __init__(self):
        CONFIG.load()
        initialize_database()
        for path in Path(self.DIRECTORY_CSV_CONVERT).glob('*.csv'):
            self._import_waon_store_to_database(path)
        self.list_csv_converter = []
        for path in Path(self.DIRECTORY_CSV_INPUT).glob('*.csv'):
            self.list_csv_converter.append(self._create_account_csv_converter(path))

    @staticmethod
    def _import_waon_store_to_database(path):
        store_kind_id = {
            ZaimCsvConverter.FILE_CSV_CONVERT_WAON: Store.STORE_KIND_WAON,
            ZaimCsvConverter.FILE_CSV_CONVERT_GOLD_POINT_CARD_PLUS: Store.STORE_KIND_GOLD_POINT_CARD_PLUS
        }.get(path.name)
        if store_kind_id is None:
            raise TypeError(f'File name "{path.name}" is not supported store name.')
        with open(path, 'r', encoding='UTF-8') as file_store:
            reader_store = csv.reader(file_store)
            stores = []
            for list_row_store in reader_store:
                list_row_store.insert(0, store_kind_id)
                stores.append(Store(*list_row_store))
            with SessionManager() as session_manager:
                session_manager.save_stores(stores)

    @staticmethod
    def _create_account_csv_converter(path):
        from zaimcsvconverter.waon.waon_csv_converter import WaonCsvConverter
        if re.search(u'.*waon.*\.csv', path.name):
            return WaonCsvConverter(path)
        elif re.search(u'.*gold_point_card_plus.*\.csv', path.name):
            return GoldPointCardPlusCsvConverter(path)

    def execute(self):
        for csv_converter in self.list_csv_converter:
            csv_converter.execute()
