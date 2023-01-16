"""This module implements convert steps from GOLD POINT CARD + input row to Zaim row."""
from pathlib import Path
from typing import cast, Optional

from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.converters.recordtozaim import (
    CsvRecordToZaimRowConverterFactory,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
    ZaimTransferRowConverter,
)
from zaimcsvconverter.inputtooutput.datasources.csv.data.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912RowData,
)
from zaimcsvconverter.inputtooutput.datasources.csv.records.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912Row,
)


class GoldPointCardPlus201912ZaimTransferRowConverter(
    ZaimTransferRowConverter[GoldPointCardPlus201912Row, GoldPointCardPlus201912RowData]
):
    """This class implements convert steps from GOLD POINT CARD + input row to Zaim transfer row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.gold_point_card_plus.account_name

    @property
    def cash_flow_target(self) -> Optional[str]:
        return self.input_row.store.transfer_target

    @property
    def amount(self) -> int:
        return self.input_row.payed_amount


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
        self, input_row: Kind1[GoldPointCardPlus201912Row, GoldPointCardPlus201912RowData], path_csv_file: Path
    ) -> ZaimRowConverter[GoldPointCardPlus201912Row, GoldPointCardPlus201912RowData]:
        dekinded_input_row = cast(GoldPointCardPlus201912Row, input_row)
        if dekinded_input_row.store.transfer_target:
            return GoldPointCardPlus201912ZaimTransferRowConverter(input_row)
        return GoldPointCardPlus201912ZaimPaymentRowConverter(input_row)
