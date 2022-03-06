"""This module implements convert steps from GOLD POINT CARD + input row to Zaim row."""
from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRow, GoldPointCardPlusRowData
from zaimcsvconverter.inputtooutput.converters.recordtozaim import (
    CsvRecordToZaimRowConverterFactory,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
)


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class GoldPointCardPlusZaimPaymentRowConverter(
    ZaimPaymentRowStoreConverter[GoldPointCardPlusRow, GoldPointCardPlusRowData]
):
    """This class implements convert steps from GOLD POINT CARD + input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.gold_point_card_plus.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


class GoldPointCardPlusZaimRowConverterFactory(
    CsvRecordToZaimRowConverterFactory[GoldPointCardPlusRow, GoldPointCardPlusRowData]
):
    """This class implements select steps from GOLD POINT CARD + Viewer input row to Zaim row converter."""

    # Reason: Maybe, there are no way to resolve.
    # The nearest issues: https://github.com/dry-python/returns/issues/708
    def create(  # type: ignore
        self, input_row: Kind1[GoldPointCardPlusRow, GoldPointCardPlusRowData]
    ) -> ZaimRowConverter[GoldPointCardPlusRow, GoldPointCardPlusRowData]:
        return GoldPointCardPlusZaimPaymentRowConverter(input_row)
