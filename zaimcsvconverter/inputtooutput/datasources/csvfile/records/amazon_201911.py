"""This module implements row model of Amazon.co.jp CSV version 201911."""

from typing import Any
from typing import Optional

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.amazon_201911 import Amazon201911RowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import InputItemRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import InputRow
from zaimcsvconverter.models import FileCsvConvertId
from zaimcsvconverter.models import Store
from zaimcsvconverter.models import StoreRowData


class Amazon201911Row(InputRow[Amazon201911RowData]):
    def __init__(self, row_data: Amazon201911RowData, *args: Any, **kwargs: Any) -> None:
        super().__init__(row_data, *args, **kwargs)


class Amazon201911RowToSkip(Amazon201911Row):
    @property
    def is_row_to_skip(self) -> bool:
        return True


class Amazon201911ItemRow(Amazon201911Row, InputItemRow[Amazon201911RowData]):
    """This class implements row model of Amazon.co.jp CSV."""

    def __init__(self, row_data: Amazon201911RowData) -> None:
        super().__init__(row_data, FileCsvConvert.AMAZON.value)
        self._store: Store = Store(
            FileCsvConvertId.AMAZON,
            StoreRowData("Amazon.co.jp", CONFIG.amazon.store_name_zaim),
        )

    @property
    def store(self) -> Store:
        return self._store


# Reason: Specification requires. pylint: disable=too-many-ancestors
class Amazon201911DiscountRow(Amazon201911ItemRow):
    """This class implements row model of Amazon.co.jp CSV."""

    def __init__(self, row_data: Amazon201911RowData) -> None:
        super().__init__(row_data)
        self._total_order: Optional[int] = row_data.total_order

    @property
    def total_order(self) -> int:
        if self._total_order is None:
            msg = "Total order on discount row is not allowed empty."
            raise ValueError(msg)
        return self._total_order

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.total_order,
            f"Total order in discount row is required. Total order = {self._total_order}",
        )
        return super().validate


# Reason: Specification requires. pylint: disable=too-many-ancestors
class Amazon201911ShippingHandlingRow(Amazon201911ItemRow):
    """Row model of shipping / handling of Amazon.co.jp CSV."""

    def __init__(self, row_data: Amazon201911RowData) -> None:
        super().__init__(row_data)
        self._subtotal_price_item: Optional[int] = row_data.subtotal_price_item

    @property
    def subtotal_price_item(self) -> int:
        if self._subtotal_price_item is None:
            msg = "Subtotal price item on shipping handling row is not allowed empty."
            raise ValueError(msg)
        return self._subtotal_price_item

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.subtotal_price_item,
            "Subtotal price item in Shipping handling row is required. "
            f"Subtotal price item = {self.subtotal_price_item}",
        )
        return super().validate


# Reason: Specification requires. pylint: disable=too-many-ancestors
class Amazon201911PaymentRow(Amazon201911ItemRow):
    """This class implements row model of Amazon.co.jp CSV."""

    def __init__(self, row_data: Amazon201911RowData) -> None:
        super().__init__(row_data)
        self._price: Optional[int] = row_data.price
        self._number: Optional[int] = row_data.number

    @property
    def price(self) -> int:
        if self._price is None:
            msg = "Price on payment row is not allowed empty."
            raise ValueError(msg)
        return self._price

    @property
    def number(self) -> int:
        if self._number is None:
            msg = "Number on payment row is not allowed empty."
            raise ValueError(msg)
        return self._number

    @property
    def validate(self) -> bool:
        self.stock_error(lambda: self.price, f"Price in payment row is required. Price = {self._price}")
        self.stock_error(lambda: self.number, f"Number in payment row is required. Number = {self._number}")
        return super().validate
