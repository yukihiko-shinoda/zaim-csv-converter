#!/usr/bin/env python

"""
This module implements payment row model of Zaim CSV.
"""

from typing import List, TYPE_CHECKING

from zaimcsvconverter.account_row import AccountRow
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimPaymentRow(ZaimRow):
    """
    This class implements payment row model of Zaim CSV.
    """
    METHOD: str = 'payment'

    def __init__(self, account_row: AccountRow):
        self._cash_flow_source: str = account_row.zaim_payment_cash_flow_source
        self._amount_payment: int = account_row.zaim_payment_amount_payment
        super().__init__(account_row)

    def convert_to_list(self) -> List[str]:
        return [
            self._date_string,
            self.METHOD,
            self._store.category_payment_large,
            self._store.category_payment_small,
            self._cash_flow_source,
            self.CASH_FLOW_TARGET_EMPTY,
            self.ITEM_NAME_EMPTY,
            self.NOTE_NAME_EMPTY,
            self._store.name_zaim,
            self.CURRENCY_EMPTY,
            self.AMOUNT_INCOME_EMPTY,
            self._amount_payment,
            self.AMOUNT_TRANSFER_EMPTY,
            self.BALANCE_ADJUSTMENT_EMPTY,
            self.AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY,
            self.SETTING_AGGREGATE_EMPTY
        ]
