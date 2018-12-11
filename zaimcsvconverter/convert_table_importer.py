#!/usr/bin/env python
"""This module implements importing process for convert table CSV."""
import csv
from pathlib import Path
from typing import List

from zaimcsvconverter.account import DirectoryCsv, Account
from zaimcsvconverter.models import Store, Item, StoreRowData, ItemRowData


class ConvertTableImporter:
    """This class implements importing process for convert table CSV."""
    def __init__(self, directory_csv_convert: Path = DirectoryCsv.CONVERT.value):
        self.directory_csv_convert = directory_csv_convert

    def execute(self):
        """This method executes importing process for convert table CSV"""
        for path in self.directory_csv_convert.glob('*.csv'):
            self._import_convert_table_to_database(path)

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
