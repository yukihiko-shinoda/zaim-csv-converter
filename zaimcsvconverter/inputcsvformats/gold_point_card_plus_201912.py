"""This module implements row model of GOLD POINT CARD+ CSV version 201912."""
from datetime import datetime

from pydantic.dataclasses import dataclass as pydantic_dataclass
from sqlalchemy.orm.exc import NoResultFound

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.inputcsvformats import InputStoreRow, InputStoreRowData


@pydantic_dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class GoldPointCardPlus201912RowData(InputStoreRowData):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV version 201912 row model."""

    used_date: StringToDateTime
    used_store: str
    used_amount: str
    number_of_division: str
    current_time_of_division: str
    payed_amount: int
    others: str

    @property
    def date(self) -> datetime:
        return self.used_date

    @property
    def store_name(self) -> str:
        return self.used_store


class GoldPointCardPlus201912Row(InputStoreRow[GoldPointCardPlus201912RowData]):
    """This class implements row model of GOLD POINT CARD+ CSV."""

    OTHERS_RETURN = "返品"

    def __init__(self, row_data: GoldPointCardPlus201912RowData):
        super().__init__(row_data, FileCsvConvert.GOLD_POINT_CARD_PLUS.value)
        self.payed_amount: int = row_data.payed_amount
        self.others: str = row_data.others

    @property
    def is_row_to_skip(self) -> bool:
        try:
            store = self.store
        except NoResultFound:
            return False
        return CONFIG.gold_point_card_plus.skip_amazon_row and store.is_amazon and self.others != self.OTHERS_RETURN
