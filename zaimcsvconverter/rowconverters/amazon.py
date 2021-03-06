"""This module implements convert steps from Amazon input row to Zaim row."""
from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.amazon import AmazonRow
from zaimcsvconverter.rowconverters import ZaimPaymentRowItemConverter, ZaimRowConverter, ZaimRowConverterFactory


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class AmazonZaimPaymentRowConverter(ZaimPaymentRowItemConverter[AmazonRow]):
    """This class implements convert steps from Amazon input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.amazon.payment_account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.price * self.input_row.number


class AmazonZaimRowConverterFactory(ZaimRowConverterFactory[AmazonRow]):
    """This class implements select steps from Amazon input row to Zaim row converter."""

    def create(self, input_row: AmazonRow) -> ZaimRowConverter:
        return AmazonZaimPaymentRowConverter(input_row)
