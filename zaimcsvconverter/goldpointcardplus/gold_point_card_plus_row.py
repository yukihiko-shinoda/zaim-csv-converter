#!/usr/bin/env python

"""
This module implements row model of GOLD POINT CARD+ CSV.
"""

import datetime
from typing import List, TYPE_CHECKING

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_row import AccountRow
from zaimcsvconverter.enum import Account
from zaimcsvconverter.models import Store
if TYPE_CHECKING:
    from zaimcsvconverter.zaim.zaim_payment_row import ZaimPaymentRow


class GoldPointCardPlusRow(AccountRow):
    """
    This class implements row model of GOLD POINT CARD+ CSV.
    """
    INDEX_USED_DATE: int = 0
    INDEX_USED_STORE: int = 1
    INDEX_USED_CARD: int = 2
    INDEX_PAYMENT_KIND: int = 3
    INDEX_NUMBER_OF_DIVISION: int = 4
    INDEX_SCHEDULED_PAYMENT_MONTH: int = 5
    INDEX_USED_AMOUNT: int = 6

    def __init__(self, list_row: List[str]):
        self._used_date: datetime = datetime.datetime.strptime(list_row[self.INDEX_USED_DATE], "%Y/%m/%d")
        self._used_store: Store = Store.try_to_find(Account.GOLD_POINT_CARD_PLUS, list_row[self.INDEX_USED_STORE])
        self._used_card: str = list_row[self.INDEX_USED_CARD]
        self._payment_kind: str = list_row[self.INDEX_PAYMENT_KIND]
        number_of_division = list_row[self.INDEX_NUMBER_OF_DIVISION]
        if number_of_division == '':
            number_of_division = 1
        self._number_of_division: int = int(number_of_division)
        self._scheduled_payment_month: str = list_row[self.INDEX_SCHEDULED_PAYMENT_MONTH]
        self._used_amount: int = int(list_row[self.INDEX_USED_AMOUNT])

    def convert_to_zaim_row(self) -> 'ZaimPaymentRow':
        from zaimcsvconverter.zaim.zaim_payment_row import ZaimPaymentRow
        return ZaimPaymentRow(self)

    @property
    def zaim_date(self) -> datetime:
        return self._used_date

    @property
    def zaim_store(self) -> Store:
        return self._used_store

    @property
    def zaim_income_cash_flow_target(self) -> str:
        raise ValueError('Income row for GOLD POINT CARD+ is not defined. Please confirm CSV file.')

    @property
    def zaim_income_ammount_income(self) -> int:
        raise ValueError('Income row for GOLD POINT CARD+ is not defined. Please confirm CSV file.')

    @property
    def zaim_payment_cash_flow_source(self) -> str:
        return CONFIG.gold_point_card_plus.account_name

    @property
    def zaim_payment_amount_payment(self) -> int:
        return self._used_amount

    @property
    def zaim_transfer_cash_flow_source(self) -> str:
        raise ValueError('Transfer row for GOLD POINT CARD+ is not defined. Please confirm CSV file.')

    @property
    def zaim_transfer_cash_flow_target(self) -> str:
        raise ValueError('Transfer row for GOLD POINT CARD+ is not defined. Please confirm CSV file.')

    @property
    def zaim_transfer_amount_transfer(self) -> int:
        raise ValueError('Transfer row for GOLD POINT CARD+ is not defined. Please confirm CSV file.')
