"""Zaim CSV Converter extended GOLD POINT CARD+ CSV Data model version 201912."""

from datetime import datetime

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import gold_point_card_plus_201912
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import InputStoreRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class GoldPointCardPlus201912RowData(gold_point_card_plus_201912.GoldPointCardPlus201912RowData, InputStoreRowData):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV version 201912 row model."""

    @property
    def date(self) -> datetime:
        return self.used_date

    @property
    def store_name(self) -> str:
        return self.used_store
