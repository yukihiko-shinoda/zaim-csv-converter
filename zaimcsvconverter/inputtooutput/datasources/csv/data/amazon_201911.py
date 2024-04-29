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
    def is_row_to_skip(self) -> bool:
        return self.is_billing_to_credit_card or self.is_free_kindle

    @property
    def is_entire_order(self) -> bool:
        return (
            self.item_name == self.ITEM_NAME_ENTIRE_ORDER
            and self.is_positive_total_order
            and self.ensures_not_payment
            and self.subtotal_price_item is None
            and self.ensures_not_credit_card
        )

    @property
    def is_billing_to_credit_card(self) -> bool:
        return (
            self.item_name == self.ITEM_NAME_BILLING_TO_CREDIT_CARD
            and self.credit_card_billing_date != ""
            and self.credit_card_billing_amount != ""
            and self.ensures_billing_to_credit_card
        )

    @property
    def ensures_billing_to_credit_card(self) -> bool:
        return self.ensures_not_payment and self.subtotal_price_item is None and self.total_order is None

    @property
    def is_shipping_handling(self) -> bool:
        return (
            self.item_name == self.ITEM_NAME_SHIPPING_HANDLING
            and self.total_order is None
            and self.ensures_not_payment
            and self.subtotal_price_item is not None
            and self.ensures_not_credit_card
        )

    @property
    def ensures_payment(self) -> bool:
        return self.is_positive_price and self.is_positive_number

    @property
    def ensures_not_payment(self) -> bool:
        return self.price is None and self.number is None

    @property
    def ensures_not_credit_card(self) -> bool:
        return not self.credit_card_billing_date and not self.credit_card_billing_amount

    @property
    def is_discount(self) -> bool:
        """Includes Amazon point."""
        return (
            not self.is_entire_order
            and not self.is_billing_to_credit_card
            and not self.is_shipping_handling
            and self.is_negative_total_order
        )

    @property
    def is_payment(self) -> bool:
        return (
            not self.is_entire_order
            and not self.is_billing_to_credit_card
            and not self.is_shipping_handling
            and not self.is_discount
            and self.ensures_payment
        )

    @property
    def is_free_kindle(self) -> bool:
        return (
            self.is_digital_order
            and self.price == 0
            and self.ensures_not_credit_card
            and not self.credit_card_identity
        )

    @property
    def is_digital_order(self) -> bool:
        return (
            self.status.startswith("デジタル注文:")
            and self.number == 1
            and self.is_completed_by_one_row_data
            and not self.destination
        )

    @property
    def is_completed_by_one_row_data(self) -> bool:
        return (
            self.price == self.total_order
            and self.price == self.subtotal_price_item
            and self.price == self.billing_amount
        )

    @property
    def is_positive_price(self) -> bool:
        return self.price is not None and self.price > 0

    @property
    def is_positive_number(self) -> bool:
        return self.number is not None and self.number > 0

    @property
    def is_positive_total_order(self) -> bool:
        return self.total_order is not None and self.total_order > 0

    @property
    def is_negative_total_order(self) -> bool:
        return self.total_order is not None and self.total_order < 0
