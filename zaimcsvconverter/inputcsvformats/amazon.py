"""This module implements row model of Amazon.co.jp CSV."""

from datetime import datetime
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats import InputItemRowData, InputItemRow, InputRowFactory
from zaimcsvconverter.models import Store, StoreRowData, AccountId


@dataclass
class AmazonRowData(InputItemRowData):
    """This class implements data class for wrapping list of Amazon.co.jp CSV row model."""
    _ordered_date: str
    order_id: str
    _item_name: str
    note: str
    _price: str
    _number: str
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

    @property
    def price(self) -> int:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return int(self._price)

    @property
    def number(self) -> int:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return int(self._number)

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.date,
            f'Invalid ordered date. Ordered date = {self._ordered_date}'
        )
        self.stock_error(
            lambda: self.price,
            f'Invalid price. Price = {self._price}'
        )
        self.stock_error(
            lambda: self.number,
            f'Invalid number. Number = {self._number}'
        )
        return super().validate


# pylint: disable=too-many-instance-attributes
class AmazonRow(InputItemRow):
    """This class implements row model of Amazon.co.jp CSV."""
    def __init__(self, account_id: AccountId, row_data: AmazonRowData):
        super().__init__(account_id, row_data)
        self._store: Store = Store(account_id, StoreRowData('Amazon.co.jp', CONFIG.amazon.store_name_zaim))
        self.price: int = row_data.price
        self.number: int = row_data.number

    @property
    def store(self) -> Store:
        return self._store


class AmazonRowFactory(InputRowFactory[AmazonRowData, AmazonRow]):
    """This class implements factory to create Amazon.co.jp CSV row instance."""
    def create(self, account_id: AccountId, input_row_data: AmazonRowData) -> AmazonRow:
        return AmazonRow(account_id, input_row_data)
