"""Converter from Amazon.co.jp CSV data to record model version 201911."""

from zaimcsvconverter.inputtooutput.datasources.csvfile.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.amazon_201911 import Amazon201911RowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.amazon_201911 import (
    Amazon201911DiscountRow,
    Amazon201911ItemRow,
    Amazon201911PaymentRow,
    Amazon201911Row,
    Amazon201911RowToSkip,
    Amazon201911ShippingHandlingRow,
)


class Amazon201911RowFactory(InputRowFactory[Amazon201911RowData, Amazon201911ItemRow]):
    """This class implements factory to create Amazon.co.jp CSV row instance version 201911."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: Amazon201911RowData) -> Amazon201911Row:  # type: ignore[override]
        # @see https://github.com/furyutei/amzOrderHistoryFilter/issues/3#issuecomment-543645937
        if input_row_data.is_row_to_skip:
            return Amazon201911RowToSkip(input_row_data)
        return self._create(input_row_data)

    def _create(self, input_row_data: Amazon201911RowData) -> Amazon201911ItemRow:
        if input_row_data.is_discount:
            return Amazon201911DiscountRow(input_row_data)
        if input_row_data.is_shipping_handling:
            return Amazon201911ShippingHandlingRow(input_row_data)
        if input_row_data.is_payment:
            return Amazon201911PaymentRow(input_row_data)
        msg = (
            "Cash flow kind is not supported. "
            f"Order date = {input_row_data.date}, "
            f"item name = {input_row_data.item_name}"
        )
        raise ValueError(msg)  # pragma: no cover
        # Reason: This line is insurance for future development so process must be not able to reach
