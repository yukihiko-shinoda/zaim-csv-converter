"""Zaim CSV Converter extended SF Card Viewer CSV Data model."""
from datetime import datetime

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import sf_card_viewer
from zaimcsvconverter.inputtooutput.datasources.csv.data import InputStoreRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class SFCardViewerRowData(sf_card_viewer.SFCardViewerRowData, InputStoreRowData):
    """This class implements data class for wrapping list of SF Card Viewer CSV row model."""

    @property
    def date(self) -> datetime:
        return self.used_date

    @property
    def store_name(self) -> str:
        return self.station_name_enter if self.is_auto_charge else self.station_name_exit

    @property
    def is_auto_charge(self) -> bool:
        """This property returns whether this row is auto charge or not."""
        return self.note == sf_card_viewer.Note.AUTO_CHARGE
