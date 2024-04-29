"""This module implements convert steps from GOLD POINT CARD + input row to Zaim row."""

from pathlib import Path

from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.converters.recordtozaim import (
    CsvRecordToZaimRowConverterFactory,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
)
from zaimcsvconverter.inputtooutput.datasources.csv.data.view_card import ViewCardRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.view_card import ViewCardRow, ViewCardStoreRow


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class ViewCardZaimPaymentRowConverter(ZaimPaymentRowStoreConverter[ViewCardStoreRow, ViewCardRowData]):
    """This class implements convert steps from GOLD POINT CARD + input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.view_card.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.billing_amount_current_time


class ViewCardZaimRowConverterFactory(CsvRecordToZaimRowConverterFactory[ViewCardRow, ViewCardRowData]):
    """This class implements select steps from GOLD POINT CARD + Viewer input row to Zaim row converter."""

    def create(
        self,
        # Reason: Maybe, there are no way to resolve.
        # The nearest issues: https://github.com/dry-python/returns/issues/708
        input_row: Kind1[ViewCardRow, ViewCardRowData],  # type: ignore[override]
        _path_csv_file: Path,
    ) -> ZaimRowConverter[ViewCardRow, ViewCardRowData]:
        # Reason: The returns can't detect correct type limited by if instance block.
        return ViewCardZaimPaymentRowConverter(input_row)  # type: ignore[return-value,arg-type]
