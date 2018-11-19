#!/usr/bin/env python

"""
This module implements converting steps from account CSV to Zaim CSV.
"""

import csv
from pathlib import Path
from typing import List, NoReturn
import numpy

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_csv_converter import AccountCsvConverter
from zaimcsvconverter.account_dependency import DirectoryCsv, Account
from zaimcsvconverter.models import initialize_database, Store, StoreRowData, Item, ItemRowData


class ZaimCsvConverter:
    """
    This class implements converting steps from account CSV to Zaim CSV.
    """
    FILE_NAME_ERROR = 'error.csv'

    def __init__(self):
        CONFIG.load()
        initialize_database()
        for path in Path(DirectoryCsv.CONVERT.value).glob('*.csv'):
            self._import_convert_table_to_database(path)
        self.list_csv_converter: List[AccountCsvConverter] = []
        for path in Path(DirectoryCsv.INPUT.value).glob('*.csv'):
            self.list_csv_converter.append(AccountCsvConverter(path, Account.create_by_path_csv_input(path).value))

    @staticmethod
    def _import_convert_table_to_database(path: Path):
        account = Account.create_by_path_csv_convert(path)
        with path.open('r', encoding='UTF-8') as file_convert_table:
            reader_convert_table = csv.reader(file_convert_table)
            model_class = account.value.convert_table_model_class
            row_data_class = {
                Store: StoreRowData,
                Item: ItemRowData,
            }.get(model_class)
            list_convert_table: List[model_class] = []
            for list_row_convert_table in reader_convert_table:
                list_convert_table.append(model_class(account, row_data_class(*list_row_convert_table)))
            model_class.save_all(list_convert_table)

    def execute(self) -> NoReturn:
        """
        This method executes all CSV converters.
        """
        list_undefined_store = []
        for csv_converter in self.list_csv_converter:
            try:
                csv_converter.execute()
            except KeyError:
                list_undefined_store.extend(csv_converter.list_undefined_content)
                continue
        if list_undefined_store:
            list_undefined_store = numpy.unique(list_undefined_store, axis=0).tolist()
            with open(
                    Path(DirectoryCsv.OUTPUT.value) / self.FILE_NAME_ERROR, 'w', encoding='UTF-8', newline='\n'
            ) as file_error:
                writer_error = csv.writer(file_error)
                for undefined_store in list_undefined_store:
                    writer_error.writerow(undefined_store)
            raise KeyError(f'Undefined store name in convert table CSV exists. Please check {self.FILE_NAME_ERROR}.')
