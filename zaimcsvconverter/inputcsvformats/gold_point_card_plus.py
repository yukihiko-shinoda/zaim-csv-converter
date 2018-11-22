#!/usr/bin/env python

"""
This module implements row model of GOLD POINT CARD+ CSV.
"""

from __future__ import annotations
import datetime
from typing import TYPE_CHECKING
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_row import AccountRow, AccountStoreRowData, AccountRowFactory
from zaimcsvconverter.models import Store
if TYPE_CHECKING:
    from zaimcsvconverter.account import Account
    from zaimcsvconverter.zaim_row import ZaimPaymentRow


class GoldPointCardPlusRowFactory(AccountRowFactory):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance."""
    def create(self, account: 'Account', row_data: GoldPointCardPlusRowData) -> GoldPointCardPlusRow:
        return GoldPointCardPlusRow(account, row_data)


@dataclass
class GoldPointCardPlusRowData(AccountStoreRowData):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV row model."""
    _used_date: str
    _used_store: str
    used_card: str
    payment_kind: str
    number_of_division: str
    scheduled_payment_month: str
    used_amount: str
    unknown_1: str
    unknown_2: str
    unknown_3: str
    unknown_4: str
    unknown_5: str
    unknown_6: str

    @property
    def date(self) -> datetime:
        """This property returns date as datetime."""
        return datetime.datetime.strptime(self._used_date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        """This property returns store name."""
        return self._used_store


class GoldPointCardPlusRow(AccountRow):
    """
    This class implements row model of GOLD POINT CARD+ CSV.
    """
    def __init__(self, account: 'Account', row_data: GoldPointCardPlusRowData):
        super().__init__(account)
        self._used_date: datetime = row_data.date
        self._used_store: Store = self.try_to_find_store(row_data.store_name)
        self._used_card: str = row_data.used_card
        self._payment_kind: str = row_data.payment_kind
        number_of_division = row_data.number_of_division
        if number_of_division == '':
            number_of_division = 1
        self._number_of_division: int = int(number_of_division)
        self._scheduled_payment_month: str = row_data.scheduled_payment_month
        self._used_amount: int = int(row_data.used_amount)

    @property
    def is_row_to_skip(self) -> bool:
        return CONFIG.gold_point_card_plus.skip_amazon_row and self._used_store.is_amazon

    def convert_to_zaim_row(self) -> 'ZaimPaymentRow':
        from zaimcsvconverter.zaim_row import ZaimPaymentRow
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
