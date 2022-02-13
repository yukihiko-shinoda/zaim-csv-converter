"""This module implements convert steps from Amazon input row to Zaim row."""
from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.amazon import AmazonRow, AmazonRowData
from zaimcsvconverter.rowconverters import ZaimPaymentRowItemConverter, ZaimRowConverter, ZaimRowConverterFactory


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class AmazonZaimPaymentRowConverter(ZaimPaymentRowItemConverter[AmazonRow, AmazonRowData]):
    """This class implements convert steps from Amazon input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.amazon.payment_account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.price * self.input_row.number


class AmazonZaimRowConverterFactory(ZaimRowConverterFactory[AmazonRow, AmazonRowData]):
    """This class implements select steps from Amazon input row to Zaim row converter."""

    def create(self, input_row: Kind1[AmazonRow, AmazonRowData]) -> ZaimRowConverter[AmazonRow, AmazonRowData]:
        return AmazonZaimPaymentRowConverter(input_row)
