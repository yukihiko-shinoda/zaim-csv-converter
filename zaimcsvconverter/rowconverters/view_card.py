"""This module implements convert steps from GOLD POINT CARD + input row to Zaim row."""
from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.view_card import ViewCardRow, ViewCardRowData
from zaimcsvconverter.rowconverters import (
    CsvRecordToZaimRowConverterFactory,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
)


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class ViewCardZaimPaymentRowConverter(ZaimPaymentRowStoreConverter[ViewCardRow, ViewCardRowData]):
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

    # Reason: Maybe, there are no way to resolve.
    # The nearest issues: https://github.com/dry-python/returns/issues/708
    def create(  # type: ignore
        self, input_row: Kind1[ViewCardRow, ViewCardRowData]
    ) -> ZaimRowConverter[ViewCardRow, ViewCardRowData]:
        return ViewCardZaimPaymentRowConverter(input_row)
