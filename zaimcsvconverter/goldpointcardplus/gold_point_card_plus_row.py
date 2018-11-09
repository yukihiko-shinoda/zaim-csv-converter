#!/usr/bin/env python
import datetime
import re

from zaimcsvconverter.AccountRow import AccountRow


class GoldPointCardPlusRow(AccountRow):
    INDEX_USED_DATE = 0
    INDEX_USED_STORE = 1
    INDEX_USED_CARD = 2
    INDEX_PAYMENT_KIND = 3
    INDEX_NUMBER_OF_DIVISION = 4
    INDEX_SCHEDULED_PAYMENT_MONTH = 5
    INDEX_USED_AMOUNT = 6

    def __init__(self, list_row):
        self._used_date = datetime.datetime.strptime(list_row[self.INDEX_USED_DATE], "%Y/%m/%d")
        self._used_store = list_row[self.INDEX_USED_STORE]
        self._used_card = list_row[self.INDEX_USED_CARD]
        self._payment_kind = list_row[self.INDEX_PAYMENT_KIND]
        number_of_division = list_row[self.INDEX_NUMBER_OF_DIVISION]
        if number_of_division is '':
            number_of_division = 1
        self._number_of_division = int(number_of_division)
        self._scheduled_payment_month = list_row[self.INDEX_SCHEDULED_PAYMENT_MONTH]
        self._used_amount = int(list_row[self.INDEX_USED_AMOUNT])

    def convert_to_zaim_row(self):
        from zaimcsvconverter.zaim.zaim_payment_row import ZaimPaymentRow
        return ZaimPaymentRow(self)

    @property
    def used_date(self):
        return self._used_date

    @property
    def used_store(self):
        return self._used_store

    @property
    def used_amount(self):
        return self._used_amount
