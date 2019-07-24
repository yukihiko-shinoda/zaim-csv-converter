"""This module implements convert steps from GOLD POINT CARD + input row to Zaim row."""
from typing import Type

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats import ValidatedInputRow
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRow
from zaimcsvconverter.rowconverters import ZaimPaymentRowConverter, ZaimRowConverterSelector, ZaimRowConverter


class GoldPointCardPlusZaimPaymentRowConverter(ZaimPaymentRowConverter[GoldPointCardPlusRow]):
    """This class implements convert steps from GOLD POINT CARD + input row to Zaim payment row."""
    @property
    def _cash_flow_source(self) -> str:
        return CONFIG.gold_point_card_plus.account_name

    @property
    def _amount_payment(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.validated_input_row.input_row.used_amount


class GoldPointCardPlusZaimRowConverterSelector(ZaimRowConverterSelector):
    """This class implements select steps from GOLD POINT CARD + Viewer input row to Zaim row converter."""
    def select(self, validated_input_row: ValidatedInputRow) -> Type[ZaimRowConverter]:
        return GoldPointCardPlusZaimPaymentRowConverter
