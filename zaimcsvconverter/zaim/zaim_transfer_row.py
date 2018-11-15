#!/usr/bin/env python

"""
This module implements transfer row model of Zaim CSV.
"""

from typing import List

from zaimcsvconverter.account_row import AccountRow
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimTransferRow(ZaimRow):
    """
    This class implements transfer row model of Zaim CSV.
    """
    METHOD: str = 'transfer'

    def __init__(self, account_row: AccountRow):
        self._cash_flow_source: str = account_row.zaim_transfer_cash_flow_source
        self._cash_flow_target: str = account_row.zaim_transfer_cash_flow_target
        self._amount_transfer: int = account_row.zaim_transfer_amount_transfer
        super().__init__(account_row)

    def convert_to_list(self) -> List[str]:
        return [
            self._date_string,
            self.METHOD,
            self.CATEGORY_LARGE_EMPTY,
            self.CATEGORY_SMALL_EMPTY,
            self._cash_flow_source,
            self._cash_flow_target,
            self.ITEM_NAME_EMPTY,
            self.NOTE_NAME_EMPTY,
            self._store.name_zaim,
            self.CURRENCY_EMPTY,
            self.AMOUNT_INCOME_EMPTY,
            self.AMOUNT_PAYMENT_EMPTY,
            self._amount_transfer,
            self.BALANCE_ADJUSTMENT_EMPTY,
            self.AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY,
            self.SETTING_AGGREGATE_EMPTY
        ]
