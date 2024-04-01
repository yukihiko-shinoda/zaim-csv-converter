"""Zaim CSV Converter extended GOLD POINT CARD+ CSV Data model."""

from datetime import datetime

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import gold_point_card_plus
from zaimcsvconverter.inputtooutput.datasources.csv.data import InputStoreRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class GoldPointCardPlusRowData(gold_point_card_plus.GoldPointCardPlusRowData, InputStoreRowData):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV row model."""

    @property
    def date(self) -> datetime:
        return self.used_date

    @property
    def store_name(self) -> str:
        return self.used_store
