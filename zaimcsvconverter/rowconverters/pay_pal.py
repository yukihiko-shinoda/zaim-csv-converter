"""Convert steps from PayPal input row to Zaim row."""
from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.pay_pal import PayPalRow, PayPalRowData
from zaimcsvconverter.rowconverters import (
    CsvRecordToZaimRowConverterFactory,
    ZaimPaymentRowStoreItemConverter,
    ZaimRowConverter,
)


class PayPalZaimPaymentRowConverter(ZaimPaymentRowStoreItemConverter[PayPalRow, PayPalRowData]):
    """This class implements convert steps from Amazon input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.pay_pal.payment_account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.net


class PayPalZaimRowConverterFactory(CsvRecordToZaimRowConverterFactory[PayPalRow, PayPalRowData]):
    """This class implements select steps from Amazon input row to Zaim row converter."""

    # Reason: Maybe, there are no way to resolve.
    # The nearest issues: https://github.com/dry-python/returns/issues/708
    def create(  # type: ignore
        self, input_row: Kind1[PayPalRow, PayPalRowData]
    ) -> ZaimRowConverter[PayPalRow, PayPalRowData]:
        return PayPalZaimPaymentRowConverter(input_row)
