"""This module implements row model of Amazon.co.jp CSV."""

from dataclasses import dataclass
from datetime import datetime

from pydantic.dataclasses import dataclass as pydantic_dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats import AbstractPydantic, InputItemRow, InputItemRowData, InputRowFactory
from zaimcsvconverter.inputcsvformats.custom_data_types import StringToDateTime
from zaimcsvconverter.models import FileCsvConvertId, Store, StoreRowData


@pydantic_dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class AmazonRowDataPydantic(AbstractPydantic):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV row model."""

    ordered_date: StringToDateTime
    order_id: str
    item_name: str
    note: str
    price: int
    number: int
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


@dataclass
class AmazonRowData(InputItemRowData[AmazonRowDataPydantic]):
    """This class implements data class for wrapping list of Amazon.co.jp CSV row model."""

    # Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
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

    def create_pydantic(self) -> AmazonRowDataPydantic:
        return AmazonRowDataPydantic(
            # Reason: Maybe, there are no way to specify type before converted by pydantic
            self._ordered_date,  # type: ignore
            self.order_id,
            self._item_name,
            self.note,
            self._price,  # type: ignore
            self._number,  # type: ignore
            self.subtotal_price_item,
            self.total_order,
            self.destination,
            self.status,
            self.billing_address,
            self.billing_amount,
            self.credit_card_billing_date,
            self.credit_card_billing_amount,
            self.credit_card_identity,
            self.url_order_summary,
            self.url_receipt,
            self.url_item,
        )

    @property
    def date(self) -> datetime:
        return self.pydantic.ordered_date

    @property
    def item_name(self) -> str:
        return self.pydantic.item_name

    @property
    def price(self) -> int:
        return self.pydantic.price

    @property
    def number(self) -> int:
        return self.pydantic.number

    @property
    def validate(self) -> bool:
        return super().validate


# pylint: disable=too-many-instance-attributes
class AmazonRow(InputItemRow[AmazonRowData]):
    """This class implements row model of Amazon.co.jp CSV."""

    def __init__(self, row_data: AmazonRowData):
        super().__init__(FileCsvConvert.AMAZON.value, row_data)
        self._store: Store = Store(
            FileCsvConvertId.AMAZON, StoreRowData("Amazon.co.jp", CONFIG.amazon.store_name_zaim)
        )
        self.price: int = row_data.price
        self.number: int = row_data.number

    @property
    def store(self) -> Store:
        return self._store


class AmazonRowFactory(InputRowFactory[AmazonRowData, AmazonRow]):
    """This class implements factory to create Amazon.co.jp CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: AmazonRowData) -> AmazonRow:  # type: ignore
        return AmazonRow(input_row_data)
