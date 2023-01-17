"""Converter from SF Card Viewer CSV data to record model."""
from typing import Callable

from zaimcsvconverter.config import SFCardViewerConfig
from zaimcsvconverter.data.sf_card_viewer import Note
from zaimcsvconverter.inputtooutput.datasources.csv.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.sf_card_viewer import SFCardViewerRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.sf_card_viewer import (
    SFCardViewerEnterExitRow,
    SFCardViewerEnterRow,
    SFCardViewerRow,
)


class SFCardViewerRowFactory(InputRowFactory[SFCardViewerRowData, SFCardViewerRow]):
    """This class implements factory to create SF Card Viewer CSV row instance."""

    def __init__(self, account_config: Callable[[], SFCardViewerConfig]):
        self._account_config = account_config

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: SFCardViewerRowData) -> SFCardViewerRow:  # type: ignore
        if input_row_data.note in (Note.EMPTY, Note.EXIT_BY_WINDOW):
            return SFCardViewerEnterExitRow(input_row_data, self._account_config())
        if input_row_data.note == Note.AUTO_CHARGE:
            return SFCardViewerEnterRow(input_row_data, self._account_config())
        return SFCardViewerRow(input_row_data, self._account_config())
