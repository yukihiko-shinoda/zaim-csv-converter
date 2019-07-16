"""This module implements row model of Amazon.co.jp CSV."""

from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Type
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.input_row import InputItemRowData, InputItemRow, InputRowFactory
from zaimcsvconverter.models import Store, Item, StoreRowData

if TYPE_CHECKING:
    from zaimcsvconverter.zaim_row import ZaimPaymentRow
    from zaimcsvconverter.account import Account


@dataclass
class AmazonRowData(InputItemRowData):
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
        return datetime.strptime(self._ordered_date, "%Y/%m/%d")

    @property
    def item_name(self) -> str:
        return self._item_name


class AmazonRowFactory(InputRowFactory[AmazonRowData]):
    """This class implements factory to create Amazon.co.jp CSV row instance."""
    def create(self, account: 'Account', row_data: AmazonRowData) -> AmazonRow:
        return AmazonRow(account, row_data)


# pylint: disable=too-many-instance-attributes
class AmazonRow(InputItemRow):
    """
    This class implements row model of Amazon.co.jp CSV.
    """
    def __init__(self, account: Account, row_data: AmazonRowData):
        super().__init__(account, row_data)
        self._store: Store = Store(account, StoreRowData('Amazon.co.jp', CONFIG.amazon.store_name_zaim))
        self._item: Optional[Item] = self.try_to_find_item(row_data.item_name)
        self.price: int = int(row_data.price)
        self.number: int = int(row_data.number)

    def zaim_row_class_to_convert(self, store: Store) -> Type['ZaimPaymentRow']:
        from zaimcsvconverter.zaim_row import ZaimPaymentRow
        return ZaimPaymentRow

    @property
    def zaim_store(self) -> Store:
        return self._store

    @property
    def zaim_item(self) -> Optional[Item]:
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
