#!/usr/bin/env python
import csv
import re
from pathlib import Path
from typing import List, NoReturn

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_csv_converter import AccountCsvConverter
from zaimcsvconverter.enum import DirectoryCsv, Account, FileCsvConvert
from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_csv_converter import GoldPointCardPlusCsvConverter
from zaimcsvconverter.models import initialize_database, Store
from zaimcsvconverter.mufg.mufg_csv_converter import MufgCsvConverter


class ZaimCsvConverter(object):
    def __init__(self):
        CONFIG.load()
        initialize_database()
        for path in Path(DirectoryCsv.CONVERT.value).glob('*.csv'):
            self._import_store_to_database(path)
        self.list_csv_converter: List[AccountCsvConverter] = []
        for path in Path(DirectoryCsv.INPUT.value).glob('*.csv'):
            self.list_csv_converter.append(self._create_account_csv_converter(path))

    @staticmethod
    def _import_store_to_database(path: Path):
        try:
            file_csv_convert = FileCsvConvert(path.name)
        except ValueError as e:
            # TODO Errorの型を詳細にチェックする
            raise ValueError(f'File name "{path.name}" is not supported store name.') from e

        account: Account = Account.create(file_csv_convert)
        with path.open('r', encoding='UTF-8') as file_store:
            reader_store = csv.reader(file_store)
            stores: List[Store] = []
            for list_row_store in reader_store:
                stores.append(Store(account, list_row_store))
            Store.save_all(stores)

    @staticmethod
    def _create_account_csv_converter(path: Path) -> AccountCsvConverter:
        from zaimcsvconverter.waon.waon_csv_converter import WaonCsvConverter
        if re.search(u'.*waon.*\.csv', path.name):
            return WaonCsvConverter(path)
        elif re.search(u'.*gold_point_card_plus.*\.csv', path.name):
            return GoldPointCardPlusCsvConverter(path)
        elif re.search(u'.*mufg.*\.csv', path.name):
            return MufgCsvConverter(path)
        else:
            raise TypeError('can\'t detect account type by csv file name. Please confirm csv file name.')

    def execute(self) -> NoReturn:
        for csv_converter in self.list_csv_converter:
            csv_converter.execute()
