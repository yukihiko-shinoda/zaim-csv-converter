"""Zaim CSV Converter extended Amazon.co.jp CSV Data model version 201911."""
from datetime import datetime

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import amazon_201911
from zaimcsvconverter.inputtooutput.datasources.csv.data import InputItemRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class Amazon201911RowData(amazon_201911.Amazon201911RowData, InputItemRowData):
    """This class implements data class for wrapping list of Amazon.co.jp CSV version 201911 row model."""

    @property
    def date(self) -> datetime:
        return self.ordered_date

    @property
    def item_name(self) -> str:
        return self.item_name_

    @property
    def is_entire_order(self) -> bool:
        return (
            self.item_name == self.ITEM_NAME_ENTIRE_ORDER
            and self.price is None
            and self.number is None
            and self.subtotal_price_item is None
            and self.total_order is not None
            and self.total_order > 0
            and not self.credit_card_billing_date
            and not self.credit_card_billing_amount
        )

    @property
    def is_billing_to_credit_card(self) -> bool:
        return (
            self.item_name == self.ITEM_NAME_BILLING_TO_CREDIT_CARD
            and self.price is None
            and self.number is None
            and self.subtotal_price_item is None
            and self.total_order is None
            # Reason:
            # When fix `return a and b != ""` as `return a and b`, mypy will report warning:
            #   error: Incompatible return value type
            #          (got "Union[Literal[False], str]", expected "bool")  [return-value]
            and self.credit_card_billing_date != ""  # noqa: PLC1901
            and self.credit_card_billing_amount != ""  # noqa: PLC1901
        )

    @property
    def is_shipping_handling(self) -> bool:
        return (
            self.item_name == self.ITEM_NAME_SHIPPING_HANDLING
            and self.price is None
            and self.number is None
            and self.subtotal_price_item is not None
            and self.total_order is None
            and not self.credit_card_billing_date
            and not self.credit_card_billing_amount
        )

    @property
    def is_discount(self) -> bool:
        # Includes Amazon point
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
            and not self.destination
            and self.status.startswith("デジタル注文:")
            and self.billing_amount == "0"
            and not self.credit_card_billing_date
            and not self.credit_card_billing_amount
            and not self.credit_card_identity
        )
