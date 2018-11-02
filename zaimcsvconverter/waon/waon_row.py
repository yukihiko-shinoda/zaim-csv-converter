#!/usr/bin/env python
from abc import ABCMeta, abstractmethod
import datetime
import re


class WaonRow(metaclass=ABCMeta):
    INDEX_DATE = 0
    INDEX_STORE = 1
    INDEX_AMOUNT = 2
    INDEX_USE_KIND = 3
    INDEX_CHARGE_KIND = 4

    def __init__(self, list_row_waon):
        self._date = datetime.datetime.strptime(list_row_waon[self.INDEX_DATE], "%Y/%m/%d")
        self._use_store = list_row_waon[self.INDEX_STORE]
        amount = re.search(u'([\d,]+)円', list_row_waon[self.INDEX_AMOUNT])
        self._use_amount = int(amount.group(1).replace(',', ''))
        self._use_kind = list_row_waon[self.INDEX_USE_KIND]
        self._charge_kind = list_row_waon[self.INDEX_CHARGE_KIND]

    @abstractmethod
    def convert_to_zaim_row(self, connection):
        pass

    @property
    def use_store(self):
        return self._use_store

    @property
    def date(self):
        return self._date

    @property
    def use_amount(self):
        return self._use_amount
