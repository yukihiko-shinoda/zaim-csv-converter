"""This module implements row model of Amazon.co.jp CSV."""

from datetime import datetime

from pydantic.dataclasses import dataclass as pydantic_dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.inputcsvformats import InputItemRow, InputItemRowData, InputRowFactory
from zaimcsvconverter.models import FileCsvConvertId, Store, StoreRowData


@pydantic_dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class AmazonRowData(InputItemRowData):
    """This class implements data class for wrapping list of Amazon.co.jp CSV row model."""

    ordered_date: StringToDateTime
    order_id: str
    item_name_: str
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

    @property
    def date(self) -> datetime:
        return self.ordered_date

    @property
    def item_name(self) -> str:
        return self.item_name_


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
