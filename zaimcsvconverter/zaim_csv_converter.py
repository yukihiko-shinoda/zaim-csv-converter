#!/usr/bin/env python

"""
This module implements converting steps from account CSV to Zaim CSV.
"""

import csv
from pathlib import Path
from typing import List, NoReturn

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_csv_converter import AccountCsvConverter
from zaimcsvconverter.enum import DirectoryCsv, Account, FileCsvConvert
from zaimcsvconverter.models import initialize_database, Store, StoreRowData
from zaimcsvconverter.recipe import Recipe


class ZaimCsvConverter:
    """
    This class implements converting steps from account CSV to Zaim CSV.
    """
    def __init__(self):
        CONFIG.load()
        initialize_database()
        for path in Path(DirectoryCsv.CONVERT.value).glob('*.csv'):
            self._import_store_to_database(path)
        self.list_csv_converter: List[AccountCsvConverter] = []
        for path in Path(DirectoryCsv.INPUT.value).glob('*.csv'):
            self.list_csv_converter.append(AccountCsvConverter(Recipe.create(path)))

    @staticmethod
    def _import_store_to_database(path: Path):
        try:
            file_csv_convert = FileCsvConvert(path.name)
        except ValueError as error:
            raise ValueError(f'File name "{path.name}" is not supported store name.') from error

        account: Account = Account.create(file_csv_convert)
        with path.open('r', encoding='UTF-8') as file_store:
            reader_store = csv.reader(file_store)
            stores: List[Store] = []
            for list_row_store in reader_store:
                stores.append(Store(account, StoreRowData(*list_row_store)))
            Store.save_all(stores)

    def execute(self) -> NoReturn:
        """
        This method executes all CSV converters.
        """
        for csv_converter in self.list_csv_converter:
            csv_converter.execute()
