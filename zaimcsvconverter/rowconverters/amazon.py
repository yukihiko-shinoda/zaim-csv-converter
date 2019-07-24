"""This module implements convert steps from Amazon input row to Zaim row."""
from typing import Type

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats import ValidatedInputRow
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
        input_row = self.validated_input_row.input_row
        return input_row.price * input_row.number


class AmazonZaimRowConverterSelector(ZaimRowConverterSelector):
    """This class implements select steps from Amazon input row to Zaim row converter."""
    def select(self, validated_input_row: ValidatedInputRow) -> Type[ZaimRowConverter]:
        return AmazonZaimPaymentRowConverter
