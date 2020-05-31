"""This module implements convert steps from GOLD POINT CARD + input row to Zaim row."""
from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.gold_point_card_plus_201912 import GoldPointCardPlus201912Row
from zaimcsvconverter.rowconverters import ZaimPaymentRowStoreConverter, ZaimRowConverter, ZaimRowConverterFactory


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class GoldPointCardPlus201912ZaimPaymentRowConverter(ZaimPaymentRowStoreConverter[GoldPointCardPlus201912Row]):
    """This class implements convert steps from GOLD POINT CARD + input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.gold_point_card_plus.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.payed_amount


class GoldPointCardPlus201912ZaimRowConverterFactory(ZaimRowConverterFactory[GoldPointCardPlus201912Row]):
    """This class implements select steps from GOLD POINT CARD + Viewer input row to Zaim row converter."""

    def create(self, input_row: GoldPointCardPlus201912Row) -> ZaimRowConverter:
        return GoldPointCardPlus201912ZaimPaymentRowConverter(input_row)
