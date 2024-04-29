"""Zaim CSV Converter extended WAON CSV Data model."""

from datetime import datetime

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import waon
from zaimcsvconverter.inputtooutput.datasources.csv.data import InputStoreRowData


@dataclass
class WaonRowData(waon.WaonRowData, InputStoreRowData):
    """This class implements data class for wrapping list of WAON CSV row model."""

    @property
    def date(self) -> datetime:
        return self.date_

    @property
    def store_name(self) -> str:
        return self.used_store
