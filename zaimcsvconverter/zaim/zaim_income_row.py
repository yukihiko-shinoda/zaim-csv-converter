#!/usr/bin/env python

"""
This module implements income row model of Zaim CSV.
"""

from typing import List

from zaimcsvconverter.account_row import AccountRow
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimIncomeRow(ZaimRow):
    """
    This class implements income row model of Zaim CSV.
    """
    METHOD: str = 'income'

    def __init__(self, account_row: AccountRow):
        self._cash_flow_target: str = account_row.zaim_income_cash_flow_target
        self._amount_income: int = account_row.zaim_income_ammount_income
        super().__init__(account_row)

    def convert_to_list(self) -> List[str]:
        return [
            self._date_string,
            self.METHOD,
            self._store.category_income,
            self.CATEGORY_SMALL_EMPTY,
            self.CASH_FLOW_SOURCE_EMPTY,
            self._cash_flow_target,
            self.ITEM_NAME_EMPTY,
            self.NOTE_NAME_EMPTY,
            self._store.name_zaim,
            self.CURRENCY_EMPTY,
            self._amount_income,
            self.AMOUNT_PAYMENT_EMPTY,
            self.AMOUNT_TRANSFER_EMPTY,
            self.BALANCE_ADJUSTMENT_EMPTY,
            self.AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY,
            self.SETTING_AGGREGATE_EMPTY
        ]
