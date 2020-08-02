"""This module implements row model of Amazon.co.jp CSV."""

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, Optional

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats import InputItemRow, InputItemRowData, InputRowFactory
from zaimcsvconverter.models import FileCsvConvertId, Store, StoreRowData


@dataclass
class Amazon201911RowData(InputItemRowData):
    """This class implements data class for wrapping list of Amazon.co.jp CSV row model."""

    # Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
    ITEM_NAME_ENTIRE_ORDER: ClassVar[str] = "（注文全体）"
    ITEM_NAME_BILLING_TO_CREDIT_CARD: ClassVar[str] = "（クレジットカードへの請求）"
    ITEM_NAME_SHIPPING_HANDLING: ClassVar[str] = "（配送料・手数料）"
    _ordered_date: str
    order_id: str
    _item_name: str
    note: str
    _price: str
    _number: str
    _subtotal_price_item: str
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
        return None if self._price == "" else int(self._price)

    @property
    def number(self) -> Optional[int]:
        return None if self._number == "" else int(self._number)

    @property
    def total_order(self) -> Optional[int]:
        return None if self._total_order == "" else int(self._total_order)

    @property
    def subtotal_price_item(self) -> Optional[int]:
        return None if self._subtotal_price_item == "" else int(self._subtotal_price_item)

    @property
    def validate(self) -> bool:
        self.stock_error(lambda: self.date, f"Invalid ordered date. Ordered date = {self._ordered_date}")
        self.stock_error(lambda: self.price, f"Invalid price. Price = {self._price}")
        self.stock_error(lambda: self.number, f"Invalid number. Number = {self._number}")
        self.stock_error(lambda: self.total_order, f"Invalid total order. Total order = {self._total_order}")
        return super().validate

    @property
    def is_entire_order(self) -> bool:
        return (
            self._item_name == self.ITEM_NAME_ENTIRE_ORDER
            and self.price is None
            and self.number is None
            and self.subtotal_price_item is None
            and self.total_order is not None
            and self.total_order > 0
            and self.credit_card_billing_date == ""
            and self.credit_card_billing_amount == ""
        )

    @property
    def is_billing_to_credit_card(self) -> bool:
        return (
            self._item_name == self.ITEM_NAME_BILLING_TO_CREDIT_CARD
            and self.price is None
            and self.number is None
            and self.subtotal_price_item is None
            and self.total_order is None
            and self.credit_card_billing_date != ""
            and self.credit_card_billing_amount != ""
        )

    @property
    def is_shipping_handling(self) -> bool:
        return (
            self._item_name == self.ITEM_NAME_SHIPPING_HANDLING
            and self.price is None
            and self.number is None
            and self.subtotal_price_item is not None
            and self.total_order is None
            and self.credit_card_billing_date == ""
            and self.credit_card_billing_amount == ""
        )

    @property
    def is_discount(self) -> bool:
        return (
            not self.is_entire_order
            and not self.is_billing_to_credit_card
            and not self.is_shipping_handling
            and self.total_order is not None
            and self.total_order < 0
        )

    @property
    def is_payment(self) -> bool:
        return (
            not self.is_entire_order
            and not self.is_billing_to_credit_card
            and not self.is_shipping_handling
            and not self.is_discount
            and self.price is not None
            and self.price > 0
            and self.number is not None
            and self.number > 0
        )

    @property
    def is_free_kindle(self) -> bool:
        return (
            self.price == 0
            and self.total_order == 0
            and self.subtotal_price_item == 0
            and self.destination == ""
            and self.status.startswith("デジタル注文:")
            and self.billing_amount == "0"
            and self.credit_card_billing_date == ""
            and self.credit_card_billing_amount == ""
            and self.credit_card_identity == ""
        )


class Amazon201911Row(InputItemRow):
    """This class implements row model of Amazon.co.jp CSV."""

    def __init__(self, row_data: Amazon201911RowData):
        super().__init__(FileCsvConvertId.AMAZON, row_data)
        self._store: Store = Store(FileCsvConvertId.AMAZON, StoreRowData("Amazon.co.jp", CONFIG.amazon.store_name_zaim))

    @property
    def store(self) -> Store:
        return self._store


class Amazon201911RowToSkip(Amazon201911Row):
    @property
    def is_row_to_skip(self) -> bool:
        return True


class Amazon201911DiscountRow(Amazon201911Row):
    """This class implements row model of Amazon.co.jp CSV."""

    def __init__(self, row_data: Amazon201911RowData):
        super().__init__(row_data)
        self._total_order: Optional[int] = row_data.total_order

    @property
    def total_order(self) -> int:
        if self._total_order is None:
            raise ValueError("Total order on discount row is not allowed empty.")
        return self._total_order

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.total_order, f"Total order in discount row is required. Total order = {self._total_order}"
        )
        return super().validate


class Amazon201911ShippingHandlingRow(Amazon201911Row):
    """Row model of shipping / handling of Amazon.co.jp CSV."""

    def __init__(self, row_data):
        super().__init__(row_data)
        self._subtotal_price_item: Optional[int] = row_data.subtotal_price_item

    @property
    def subtotal_price_item(self):
        if self._subtotal_price_item is None:
            raise ValueError("Subtotal price item on shipping handling row is not allowed empty.")
        return self._subtotal_price_item

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.subtotal_price_item,
            "Subtotal price item in Shipping handling row is required. "
            f"Subtotal price item = {self.subtotal_price_item}",
        )
        return super().validate


class Amazon201911PaymentRow(Amazon201911Row):
    """This class implements row model of Amazon.co.jp CSV."""

    def __init__(self, row_data: Amazon201911RowData):
        super().__init__(row_data)
        self._price: Optional[int] = row_data.price
        self._number: Optional[int] = row_data.number

    @property
    def price(self) -> int:
        if self._price is None:
            raise ValueError("Price on payment row is not allowed empty.")
        return self._price

    @property
    def number(self) -> int:
        if self._number is None:
            raise ValueError("Number on payment row is not allowed empty.")
        return self._number

    @property
    def validate(self) -> bool:
        self.stock_error(lambda: self.price, f"Price in payment row is required. Price = {self._price}")
        self.stock_error(lambda: self.number, f"Number in payment row is required. Number = {self._number}")
        return super().validate


class Amazon201911RowFactory(InputRowFactory[Amazon201911RowData, Amazon201911Row]):
    """This class implements factory to create Amazon.co.jp CSV row instance."""

    def create(self, input_row_data: Amazon201911RowData) -> Amazon201911Row:
        # @see https://github.com/furyutei/amzOrderHistoryFilter/issues/3#issuecomment-543645937
        if input_row_data.is_billing_to_credit_card or input_row_data.is_free_kindle:
            return Amazon201911RowToSkip(input_row_data)
        if input_row_data.is_discount:
            return Amazon201911DiscountRow(input_row_data)
        if input_row_data.is_shipping_handling:
            return Amazon201911ShippingHandlingRow(input_row_data)
        if input_row_data.is_payment:
            return Amazon201911PaymentRow(input_row_data)
        raise ValueError(
            'Cash flow kind is not supported. "'
            f'Order date = {input_row_data.date}, "'
            f'"item name = {input_row_data.item_name}'
        )  # pragma: no cover
        # Reason: This line is insurance for future development so process must be not able to reach
