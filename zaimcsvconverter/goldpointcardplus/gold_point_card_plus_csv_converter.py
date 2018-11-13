#!/usr/bin/env python
from pathlib import Path

from zaimcsvconverter.account_csv_converter import AccountCsvConverter
from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_row import GoldPointCardPlusRow


class GoldPointCardPlusCsvConverter(AccountCsvConverter):
    def __init__(self, csv_file: Path):
        super().__init__(csv_file, 'shift_jis_2004', False)

    @staticmethod
    def _create_account_row(list_row_account) -> GoldPointCardPlusRow:
        return GoldPointCardPlusRow(list_row_account)
