"""Convert steps from PayPal input row to Zaim row."""
from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.pay_pal import PayPalRow
from zaimcsvconverter.rowconverters import ZaimPaymentRowStoreItemConverter, ZaimRowConverter, ZaimRowConverterFactory


class PayPalZaimPaymentRowConverter(ZaimPaymentRowStoreItemConverter[PayPalRow]):
    """This class implements convert steps from Amazon input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.pay_pal.payment_account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.net


class PayPalZaimRowConverterFactory(ZaimRowConverterFactory[PayPalRow]):
    """This class implements select steps from Amazon input row to Zaim row converter."""

    def create(self, input_row: PayPalRow) -> ZaimRowConverter:
        return PayPalZaimPaymentRowConverter(input_row)
