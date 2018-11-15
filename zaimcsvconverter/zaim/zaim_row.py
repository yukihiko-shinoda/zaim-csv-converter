#!/usr/bin/env python

"""
This module implements abstract row model of Zaim CSV.
"""

import datetime
from abc import ABCMeta, abstractmethod
from typing import List

from zaimcsvconverter.models import Store
from zaimcsvconverter.account_row import AccountRow


# pylint: disable=too-many-instance-attributes
class ZaimRow(metaclass=ABCMeta):
    """
    This class implements abstract row model of Zaim CSV.
    """
    CATEGORY_LARGE_EMPTY = '-'
    CATEGORY_SMALL_EMPTY = '-'
    CASH_FLOW_SOURCE_EMPTY = ''
    CASH_FLOW_TARGET_EMPTY = ''
    AMOUNT_INCOME_EMPTY = 0
    AMOUNT_PAYMENT_EMPTY = 0
    AMOUNT_TRANSFER_EMPTY = 0
    ITEM_NAME_EMPTY = ''
    NOTE_NAME_EMPTY = ''
    CURRENCY_EMPTY = ''
    BALANCE_ADJUSTMENT_EMPTY = ''
    AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY = ''
    SETTING_AGGREGATE_EMPTY = ''

    @property
    def _date_string(self) -> str:
        return self._date.strftime("%Y-%m-%d")

    def __init__(self, account_row: AccountRow):
        self._date: datetime = account_row.zaim_date
        self._store: Store = account_row.zaim_store

    @abstractmethod
    def convert_to_list(self) -> List[str]:
        """
        This method converts object data to list.
        """
        pass
