"""This module implements convert steps from Amazon input row to Zaim row."""

from pathlib import Path

from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.converters.recordtozaim import CsvRecordToZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimPaymentRowItemConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimRowConverter
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.amazon_201911 import Amazon201911RowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.amazon_201911 import Amazon201911DiscountRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.amazon_201911 import Amazon201911ItemRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.amazon_201911 import Amazon201911PaymentRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.amazon_201911 import Amazon201911ShippingHandlingRow


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class Amazon201911DiscountZaimPaymentRowConverter(
    ZaimPaymentRowItemConverter[Amazon201911DiscountRow, Amazon201911RowData],
):
    """This class implements convert steps from Amazon input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.amazon.payment_account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.total_order


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class Amazon201911PaymentZaimPaymentRowConverter(
    ZaimPaymentRowItemConverter[Amazon201911PaymentRow, Amazon201911RowData],
):
    """This class implements convert steps from Amazon input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.amazon.payment_account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.price * self.input_row.number


class Amazon201911ShippingHandlingZaimPaymentRowConverter(
    ZaimPaymentRowItemConverter[Amazon201911ShippingHandlingRow, Amazon201911RowData],
):
    """This class implements convert steps from Amazon input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.amazon.payment_account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.subtotal_price_item


class Amazon201911ZaimRowConverterFactory(
    CsvRecordToZaimRowConverterFactory[Amazon201911ItemRow, Amazon201911RowData],
):
    """This class implements select steps from Amazon input row to Zaim row converter."""

    def create(
        self,
        # Reason: Maybe, there are no way to resolve.
        # The nearest issues: https://github.com/dry-python/returns/issues/708
        input_row: Kind1[Amazon201911ItemRow, Amazon201911RowData],  # type: ignore[override]
        _path_csv_file: Path,
    ) -> ZaimRowConverter[Amazon201911ItemRow, Amazon201911RowData]:
        if isinstance(input_row, Amazon201911DiscountRow):
            # Reason: The returns can't detect correct type limited by if instance block.
            return Amazon201911DiscountZaimPaymentRowConverter(input_row)  # type: ignore[arg-type,return-value]
        if isinstance(input_row, Amazon201911PaymentRow):
            # Reason: The returns can't detect correct type limited by if instance block.
            return Amazon201911PaymentZaimPaymentRowConverter(input_row)  # type: ignore[arg-type,return-value]
        if isinstance(input_row, Amazon201911ShippingHandlingRow):
            # Reason: The returns can't detect correct type limited by if instance block.
            return Amazon201911ShippingHandlingZaimPaymentRowConverter(
                input_row,  # type: ignore[arg-type,return-value]
            )
        msg = f"Unsupported row. class = {type(input_row)}"
        raise ValueError(msg)  # pragma: no cover
