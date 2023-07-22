"""Converter from Mobile Suica CSV data to record model."""
from typing import Callable

from zaimcsvconverter.config import SFCardViewerConfig
from zaimcsvconverter.inputtooutput.datasources.csv.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.mobile_suica import MobileSuicaRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.mobile_suica import (
    MobileSuicaBusEtCeteraRow,
    MobileSuicaEnterExitRow,
    MobileSuicaFirstRow,
    MobileSuicaRow,
    MobileSuicaStoreRow,
)


class MobileSuicaRowFactory(InputRowFactory[MobileSuicaRowData, MobileSuicaRow]):
    """This class implements factory to create Mobile Suica CSV row instance."""

    def __init__(self, account_config: Callable[[], SFCardViewerConfig]) -> None:
        self._account_config = account_config

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: MobileSuicaRowData) -> MobileSuicaRow:  # type: ignore[override]
        input_row_data: MobileSuicaRowData = input_row_data
        if input_row_data.has_kind_2:
            return MobileSuicaEnterExitRow(input_row_data, self._account_config())
        if input_row_data.is_bus_et_cetera:
            return MobileSuicaBusEtCeteraRow(input_row_data, self._account_config())
        if input_row_data.first_record:
            return MobileSuicaFirstRow(input_row_data, self._account_config())
        if input_row_data.has_used_place_1:
            return MobileSuicaStoreRow(input_row_data, self._account_config())
        return MobileSuicaRow(input_row_data, self._account_config())
