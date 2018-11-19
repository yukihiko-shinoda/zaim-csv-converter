#!/usr/bin/env python

"""
This module implements row model of Amazon.co.jp CSV.
"""

from __future__ import annotations
import datetime
from typing import TYPE_CHECKING
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_row import AccountItemRowData, AccountItemRow
from zaimcsvconverter.models import Store, Item, StoreRowData
from zaimcsvconverter.unility import Utility

if TYPE_CHECKING:
    from zaimcsvconverter.zaim_row import ZaimPaymentRow


@dataclass
class AmazonRowData(AccountItemRowData):
    """This class implements data class for wrapping list of Amazon.co.jp CSV row model."""
    _ordered_date: str
    order_id: str
    _item_name: str
    note: str
    price: str
    number: str
    subtotal_price_item: str
    total_order: str
    destination: str
    status: str
    billing_address: str
    billing_amount: str
    credit_card_billing_date: str
    credit_card_billing_amount: str
    credit_card_identity: str
    url_order_summary: str
    url_receipt: str
    url_item: str

    @property
    def date(self) -> datetime:
        """This property returns date as datetime."""
        return datetime.datetime.strptime(self._ordered_date, "%Y/%m/%d")

    @property
    def item_name(self) -> str:
        """This property returns store name."""
        return self._item_name


# pylint: disable=too-many-instance-attributes
class AmazonRow(AccountItemRow):
    """
    This class implements row model of Amazon.co.jp CSV.
    """
    def __init__(self, row_data: AmazonRowData):
        from zaimcsvconverter.account_dependency import Account
        self._ordered_date: datetime = row_data.date
        self._store: Store = Store(Account.AMAZON, StoreRowData('Amazon.co.jp', CONFIG.amazon.store_name_zaim))
        self.order_id: str = row_data.order_id
        self._item: Item = self.try_to_find_item(row_data.item_name)
        self.note: str = row_data.note
        self.price: int = int(row_data.price)
        self.number: int = int(row_data.number)
        self.subtotal_price_item: int = Utility.convert_string_to_int_or_none(row_data.subtotal_price_item)
        self.total_order: int = Utility.convert_string_to_int_or_none(row_data.total_order)
        self.destination: str = row_data.destination
        self.status: str = row_data.status
        self.billing_address: str = row_data.billing_address
        self.billing_amount: int = Utility.convert_string_to_int_or_none(row_data.billing_amount)
        self.credit_card_billing_date: str = row_data.credit_card_billing_date
        self.credit_card_billing_amount: int = Utility.convert_string_to_int_or_none(
            row_data.credit_card_billing_amount)
        self.credit_card_identity: str = row_data.credit_card_identity
        self.url_order_summary: str = row_data.url_order_summary
        self.url_receipt: str = row_data.url_receipt
        self.url_item: str = row_data.url_item

    def convert_to_zaim_row(self) -> 'ZaimPaymentRow':
        from zaimcsvconverter.zaim_row import ZaimPaymentRow
        return ZaimPaymentRow(self)

    @property
    def zaim_date(self) -> datetime:
        return self._ordered_date

    @property
    def zaim_store(self) -> Store:
        return self._store

    @property
    def zaim_item(self) -> Item:
        return self._item

    @property
    def zaim_income_cash_flow_target(self) -> str:
        raise ValueError('Income row for Amazon.co.jp is not defined. Please confirm CSV file.')

    @property
    def zaim_income_ammount_income(self) -> int:
        raise ValueError('Income row for Amazon.co.jp is not defined. Please confirm CSV file.')

    @property
    def zaim_payment_cash_flow_source(self) -> str:
        return CONFIG.amazon.payment_account_name

    @property
    def zaim_payment_amount_payment(self) -> int:
        return self.price * self.number

    @property
    def zaim_transfer_cash_flow_source(self) -> str:
        raise ValueError('Transfer row for Amazon.co.jp is not defined. Please confirm CSV file.')

    @property
    def zaim_transfer_cash_flow_target(self) -> str:
        raise ValueError('Transfer row for Amazon.co.jp is not defined. Please confirm CSV file.')

    @property
    def zaim_transfer_amount_transfer(self) -> int:
        raise ValueError('Transfer row for Amazon.co.jp is not defined. Please confirm CSV file.')

    @staticmethod
    def create(row_data: AmazonRowData) -> AmazonRow:
        return AmazonRow(row_data)
