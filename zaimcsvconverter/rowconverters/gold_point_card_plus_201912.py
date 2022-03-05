"""This module implements convert steps from GOLD POINT CARD + input row to Zaim row."""
from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912Row,
    GoldPointCardPlus201912RowData,
)
from zaimcsvconverter.rowconverters import (
    CsvRecordToZaimRowConverterFactory,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
)


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class GoldPointCardPlus201912ZaimPaymentRowConverter(
    ZaimPaymentRowStoreConverter[GoldPointCardPlus201912Row, GoldPointCardPlus201912RowData]
):
    """This class implements convert steps from GOLD POINT CARD + input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.gold_point_card_plus.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.payed_amount


class GoldPointCardPlus201912ZaimRowConverterFactory(
    CsvRecordToZaimRowConverterFactory[GoldPointCardPlus201912Row, GoldPointCardPlus201912RowData]
):
    """This class implements select steps from GOLD POINT CARD + Viewer input row to Zaim row converter."""

    # Reason: Maybe, there are no way to resolve.
    # The nearest issues: https://github.com/dry-python/returns/issues/708
    def create(  # type: ignore
        self, input_row: Kind1[GoldPointCardPlus201912Row, GoldPointCardPlus201912RowData]
    ) -> ZaimRowConverter[GoldPointCardPlus201912Row, GoldPointCardPlus201912RowData]:
        return GoldPointCardPlus201912ZaimPaymentRowConverter(input_row)
