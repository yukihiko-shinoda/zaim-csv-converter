#!/usr/bin/env python

"""This module implements row model of GOLD POINT CARD+ CSV."""

from __future__ import annotations
import datetime
from typing import TYPE_CHECKING
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.input_row import InputStoreRowData, InputRowFactory, InputStoreRow
if TYPE_CHECKING:
    from zaimcsvconverter.account import Account
    from zaimcsvconverter.zaim_row import ZaimPaymentRow


class GoldPointCardPlusRowFactory(InputRowFactory):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance."""
    def create(self, account: 'Account', row_data: GoldPointCardPlusRowData) -> GoldPointCardPlusRow:
        return GoldPointCardPlusRow(account, row_data)


@dataclass
class GoldPointCardPlusRowData(InputStoreRowData):
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
        return datetime.datetime.strptime(self._used_date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        return self._used_store


class GoldPointCardPlusRow(InputStoreRow):
    """This class implements row model of GOLD POINT CARD+ CSV."""
    def __init__(self, account: 'Account', row_data: GoldPointCardPlusRowData):
        super().__init__(account, row_data)
        self._used_amount: int = int(row_data.used_amount)

    @property
    def is_row_to_skip(self) -> bool:
        return CONFIG.gold_point_card_plus.skip_amazon_row and self.zaim_store.is_amazon

    def convert_to_zaim_row(self) -> 'ZaimPaymentRow':
        from zaimcsvconverter.zaim_row import ZaimPaymentRow
        return ZaimPaymentRow(self)

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
