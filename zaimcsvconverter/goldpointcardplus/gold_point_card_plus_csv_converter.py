#!/usr/bin/env python

"""
This module implements converting steps for GOLD POINT CARD+ CSV.
"""

from pathlib import Path

from zaimcsvconverter.account_csv_converter import AccountCsvConverter
from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_row import GoldPointCardPlusRow


class GoldPointCardPlusCsvConverter(AccountCsvConverter):
    """
    This class implements converting steps for GOLD POINT CARD+ CSV.
    """
    def __init__(self, csv_file: Path):
        super().__init__(csv_file, 'shift_jis_2004', False)

    @staticmethod
    def _create_account_row(list_row_account) -> GoldPointCardPlusRow:
        return GoldPointCardPlusRow(list_row_account)
