"""This module implements convert steps from GOLD POINT CARD + input row to Zaim row."""
from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.view_card import ViewCardRow, ViewCardRowData
from zaimcsvconverter.rowconverters import ZaimPaymentRowStoreConverter, ZaimRowConverter, ZaimRowConverterFactory


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


class ViewCardZaimRowConverterFactory(ZaimRowConverterFactory[ViewCardRow, ViewCardRowData]):
    """This class implements select steps from GOLD POINT CARD + Viewer input row to Zaim row converter."""

    def create(self, input_row: Kind1[ViewCardRow, ViewCardRowData]) -> ZaimRowConverter[ViewCardRow, ViewCardRowData]:
        return ViewCardZaimPaymentRowConverter(input_row)
