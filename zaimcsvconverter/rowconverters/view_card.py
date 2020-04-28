"""This module implements convert steps from GOLD POINT CARD + input row to Zaim row."""
from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.view_card import ViewCardRow
from zaimcsvconverter.rowconverters import ZaimPaymentRowStoreConverter, ZaimRowConverterFactory, ZaimRowConverter


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class ViewCardZaimPaymentRowConverter(ZaimPaymentRowStoreConverter[ViewCardRow]):
    """This class implements convert steps from GOLD POINT CARD + input row to Zaim payment row."""
    @property
    def cash_flow_source(self) -> str:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        return CONFIG.view_card.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.billing_amount_current_time


class ViewCardZaimRowConverterFactory(ZaimRowConverterFactory[ViewCardRow]):
    """This class implements select steps from GOLD POINT CARD + Viewer input row to Zaim row converter."""
    def create(self, input_row: ViewCardRow) -> ZaimRowConverter:
        return ViewCardZaimPaymentRowConverter(input_row)
