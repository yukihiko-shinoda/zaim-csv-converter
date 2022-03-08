"""Amazon.co.jp CSV Data model version 201911."""
from typing import ClassVar

from pydantic.dataclasses import dataclass

from zaimcsvconverter.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.customdatatypes.string_to_optional_int import ConstrainedStringToOptionalInt
from zaimcsvconverter.first_form_normalizer import CsvRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class Amazon201911RowData(CsvRowData):
    """This class implements data class for wrapping list of Amazon.co.jp CSV version 201911 row model."""

    # Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
    ITEM_NAME_ENTIRE_ORDER: ClassVar[str] = "（注文全体）"
    ITEM_NAME_BILLING_TO_CREDIT_CARD: ClassVar[str] = "（クレジットカードへの請求）"
    ITEM_NAME_SHIPPING_HANDLING: ClassVar[str] = "（配送料・手数料）"
    ordered_date: StringToDateTime
    order_id: str
    item_name_: str
    note: str
    price: ConstrainedStringToOptionalInt
    number: ConstrainedStringToOptionalInt
    subtotal_price_item: ConstrainedStringToOptionalInt
    total_order: ConstrainedStringToOptionalInt
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
