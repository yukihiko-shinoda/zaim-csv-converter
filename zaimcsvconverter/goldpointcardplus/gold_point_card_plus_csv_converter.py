#!/usr/bin/env python
from zaimcsvconverter.AccountCsvConverter import AccountCsvConverter
from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_row import GoldPointCardPlusRow


class GoldPointCardPlusCsvConverter(AccountCsvConverter):
    def __init__(self, csv_file):
        super().__init__(csv_file, 'shift_jis', False)

    def _create_account_row(self, list_row_account):
        return GoldPointCardPlusRow(list_row_account)
