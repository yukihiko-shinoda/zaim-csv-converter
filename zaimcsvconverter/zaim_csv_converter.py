#!/usr/bin/env python
"""This module implements converting steps from account CSV to Zaim CSV."""
from typing import NoReturn

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_csv_converter_iterator import AccountCsvConverterIterator
from zaimcsvconverter.convert_table_importer import ConvertTableImporter
from zaimcsvconverter.models import initialize_database


class ZaimCsvConverter:
    """This class implements converting steps from account CSV to Zaim CSV."""
    @staticmethod
    def execute() -> NoReturn:
        """This method executes all CSV converters."""
        CONFIG.load()
        initialize_database()
        ConvertTableImporter().execute()
        AccountCsvConverterIterator().execute()
