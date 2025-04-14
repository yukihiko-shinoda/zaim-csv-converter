"""This module implements convert steps from GOLD POINT CARD + input row to Zaim row."""

from pathlib import Path

from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.converters.recordtozaim import (
    CsvRecordToZaimRowConverterFactory,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
)
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.gold_point_card_plus import GoldPointCardPlusRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.gold_point_card_plus import GoldPointCardPlusRow


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class GoldPointCardPlusZaimPaymentRowConverter(
    ZaimPaymentRowStoreConverter[GoldPointCardPlusRow, GoldPointCardPlusRowData],
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
    CsvRecordToZaimRowConverterFactory[GoldPointCardPlusRow, GoldPointCardPlusRowData],
):
    """This class implements select steps from GOLD POINT CARD + Viewer input row to Zaim row converter."""

    def create(
        self,
        # Reason: Maybe, there are no way to resolve.
        # The nearest issues: https://github.com/dry-python/returns/issues/708
        input_row: Kind1[GoldPointCardPlusRow, GoldPointCardPlusRowData],  # type: ignore[override]
        _path_csv_file: Path,
    ) -> ZaimRowConverter[GoldPointCardPlusRow, GoldPointCardPlusRowData]:
        return GoldPointCardPlusZaimPaymentRowConverter(input_row)
