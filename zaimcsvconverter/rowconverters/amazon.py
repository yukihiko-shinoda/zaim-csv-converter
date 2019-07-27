"""This module implements convert steps from Amazon input row to Zaim row."""
from typing import Type

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.amazon import AmazonRow
from zaimcsvconverter.rowconverters import ZaimPaymentRowConverter, ZaimRowConverterSelector, ZaimRowConverter


class AmazonZaimPaymentRowConverter(ZaimPaymentRowConverter[AmazonRow]):
    """This class implements convert steps from Amazon input row to Zaim payment row."""
    @property
    def _cash_flow_source(self) -> str:
        return CONFIG.amazon.payment_account_name

    @property
    def _amount_payment(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.price * self.input_row.number


class AmazonZaimRowConverterSelector(ZaimRowConverterSelector[AmazonRow]):
    """This class implements select steps from Amazon input row to Zaim row converter."""
    def select(self, input_row: AmazonRow) -> Type[ZaimRowConverter]:
        return AmazonZaimPaymentRowConverter
