"""This module implements convert steps from Amazon input row to Zaim row."""
from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.amazon_201911 import (
    Amazon201911DiscountRow,
    Amazon201911PaymentRow,
    Amazon201911Row,
    Amazon201911ShippingHandlingRow,
)
from zaimcsvconverter.rowconverters import ZaimPaymentRowItemConverter, ZaimRowConverter, ZaimRowConverterFactory


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class Amazon201911DiscountZaimPaymentRowConverter(ZaimPaymentRowItemConverter[Amazon201911DiscountRow]):
    """This class implements convert steps from Amazon input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.amazon.payment_account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.total_order


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class Amazon201911PaymentZaimPaymentRowConverter(ZaimPaymentRowItemConverter[Amazon201911PaymentRow]):
    """This class implements convert steps from Amazon input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.amazon.payment_account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.price * self.input_row.number


class Amazon201911ShippingHandlingZaimPaymentRowConverter(ZaimPaymentRowItemConverter[Amazon201911ShippingHandlingRow]):
    """This class implements convert steps from Amazon input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.amazon.payment_account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.subtotal_price_item


class Amazon201911ZaimRowConverterFactory(ZaimRowConverterFactory[Amazon201911Row]):
    """This class implements select steps from Amazon input row to Zaim row converter."""

    def create(self, input_row: Amazon201911Row) -> ZaimRowConverter:
        if isinstance(input_row, Amazon201911DiscountRow):
            return Amazon201911DiscountZaimPaymentRowConverter(input_row)
        if isinstance(input_row, Amazon201911PaymentRow):
            return Amazon201911PaymentZaimPaymentRowConverter(input_row)
        if isinstance(input_row, Amazon201911ShippingHandlingRow):
            return Amazon201911ShippingHandlingZaimPaymentRowConverter(input_row)
        raise ValueError(f"Unsupported row. class = {type(input_row)}")  # pragma: no cover
