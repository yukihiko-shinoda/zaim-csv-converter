"""Amazon.co.jp CSV Data model."""
from pydantic.dataclasses import dataclass

from zaimcsvconverter.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.first_form_normalizer import CsvRowData


@dataclass
# Reason: Model, has similar designed versions.
# pylint: disable=too-few-public-methods,too-many-instance-attributes,duplicate-code
class AmazonRowData(CsvRowData):
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
