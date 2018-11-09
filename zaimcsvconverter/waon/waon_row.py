#!/usr/bin/env python
from abc import abstractmethod
import datetime
import re

from zaimcsvconverter.AccountRow import AccountRow


class WaonRow(AccountRow):
    INDEX_DATE = 0
    INDEX_USED_STORE = 1
    INDEX_USED_AMOUNT = 2
    INDEX_USED_KIND = 3
    INDEX_CHARGE_KIND = 4

    def __init__(self, list_row_waon):
        self._date = datetime.datetime.strptime(list_row_waon[self.INDEX_DATE], "%Y/%m/%d")
        self._used_store = list_row_waon[self.INDEX_USED_STORE]
        used_amount = re.search(u'([\d,]+)円', list_row_waon[self.INDEX_USED_AMOUNT])
        self._used_amount = int(used_amount.group(1).replace(',', ''))
        self._used_kind = list_row_waon[self.INDEX_USED_KIND]
        self._charge_kind = list_row_waon[self.INDEX_CHARGE_KIND]

    @abstractmethod
    def convert_to_zaim_row(self):
        pass

    @property
    def date(self):
        return self._date

    @property
    def used_store(self):
        return self._used_store

    @property
    def used_amount(self):
        return self._used_amount
