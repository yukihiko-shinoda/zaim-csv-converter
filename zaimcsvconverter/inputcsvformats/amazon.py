"""This module implements row model of Amazon.co.jp CSV."""

from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats import InputItemRowData, InputItemRow, InputRowFactory
from zaimcsvconverter.models import Store, Item, StoreRowData, AccountId


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


# pylint: disable=too-many-instance-attributes
class AmazonRow(InputItemRow):
    """This class implements row model of Amazon.co.jp CSV."""
    def __init__(self, account_id: AccountId, row_data: AmazonRowData):
        super().__init__(account_id, row_data)
        self._store: Store = Store(account_id, StoreRowData('Amazon.co.jp', CONFIG.amazon.store_name_zaim))
        self._item: Optional[Item] = self.try_to_find_item(row_data.item_name)
        self.price: int = int(row_data.price)
        self.number: int = int(row_data.number)

    @property
    def store(self) -> Store:
        return self._store


class AmazonRowFactory(InputRowFactory):
    """This class implements factory to create Amazon.co.jp CSV row instance."""
    def create(self, account_id: AccountId, row_data: AmazonRowData) -> AmazonRow:
        return AmazonRow(account_id, row_data)
