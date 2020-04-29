"""This module implements row model of Amazon.co.jp CSV."""

from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats import InputItemRowData, InputItemRow, InputRowFactory
from zaimcsvconverter.models import Store, StoreRowData, FileCsvConvertId


@dataclass
class Amazon201911RowData(InputItemRowData):
    """This class implements data class for wrapping list of Amazon.co.jp CSV row model."""
    # Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
    _ordered_date: str
    order_id: str
    _item_name: str
    note: str
    _price: str
    _number: str
    subtotal_price_item: str
    _total_order: str
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
    def price(self) -> Optional[int]:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return None if self._price == '' else int(self._price)

    @property
    def number(self) -> Optional[int]:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return None if self._number == '' else int(self._number)

    @property
    def total_order(self) -> Optional[int]:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return None if self._total_order == '' else int(self._total_order)

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
        self.stock_error(
            lambda: self.total_order,
            f'Invalid total order. Total order = {self._total_order}'
        )
        return super().validate

    @property
    def is_discount(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.total_order is not None and self.total_order < 0


class Amazon201911Row(InputItemRow):
    """This class implements row model of Amazon.co.jp CSV."""
    def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: Amazon201911RowData):
        super().__init__(file_csv_convert_id, row_data)
        self._store: Store = Store(file_csv_convert_id, StoreRowData('Amazon.co.jp', CONFIG.amazon.store_name_zaim))

    @property
    def store(self) -> Store:
        return self._store


class Amazon201911DiscountRow(Amazon201911Row):
    """This class implements row model of Amazon.co.jp CSV."""
    def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: Amazon201911RowData):
        super().__init__(file_csv_convert_id, row_data)
        self._total_order: Optional[int] = row_data.total_order

    @property
    def total_order(self) -> int:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        if self._total_order is None:
            raise ValueError('Total order on discount row is not allowed empty.')
        return self._total_order

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.total_order,
            f'Total order in discount row is required. Total order = {self._total_order}'
        )
        return super().validate


class Amazon201911PaymentRow(Amazon201911Row):
    """This class implements row model of Amazon.co.jp CSV."""
    def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: Amazon201911RowData):
        super().__init__(file_csv_convert_id, row_data)
        self._price: Optional[int] = row_data.price
        self._number: Optional[int] = row_data.number

    @property
    def price(self) -> int:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        if self._price is None:
            raise ValueError('Price on payment row is not allowed empty.')
        return self._price

    @property
    def number(self) -> int:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        if self._number is None:
            raise ValueError('Number on payment row is not allowed empty.')
        return self._number

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.price,
            f'Price in payment row is required. Price = {self._price}'
        )
        self.stock_error(
            lambda: self.number,
            f'Number in payment row is required. Number = {self._number}'
        )
        return super().validate


class Amazon201911RowFactory(InputRowFactory[Amazon201911RowData, Amazon201911Row]):
    """This class implements factory to create Amazon.co.jp CSV row instance."""
    def create(self, file_csv_convert_id: FileCsvConvertId, input_row_data: Amazon201911RowData) -> Amazon201911Row:
        # @see https://github.com/furyutei/amzOrderHistoryFilter/issues/3#issuecomment-543645937
        if input_row_data.is_discount:
            return Amazon201911DiscountRow(file_csv_convert_id, input_row_data)
        return Amazon201911PaymentRow(file_csv_convert_id, input_row_data)
