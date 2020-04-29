"""This module implements row model of GOLD POINT CARD+ CSV version 201912."""
from datetime import datetime
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats import InputStoreRowData, InputStoreRow, InputRowFactory
from zaimcsvconverter.models import FileCsvConvertId


@dataclass
class GoldPointCardPlus201912RowData(InputStoreRowData):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV version 201912 row model."""
    _used_date: str
    _used_store: str
    _used_amount: str
    _number_of_division: str
    _current_time_of_division: str
    _payed_amount: str
    _others: str

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._used_date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        return self._used_store

    @property
    def payed_amount(self) -> int:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return int(self._payed_amount)

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.date,
            f'Invalid used date. Used date = {self._used_date}'
        )
        self.stock_error(
            lambda: self.payed_amount,
            f'Invalid used amount. Used amount = {self._used_amount}'
        )
        return super().validate


class GoldPointCardPlus201912Row(InputStoreRow):
    """This class implements row model of GOLD POINT CARD+ CSV."""
    def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: GoldPointCardPlus201912RowData):
        super().__init__(file_csv_convert_id, row_data)
        self.payed_amount: int = row_data.payed_amount

    @property
    def is_row_to_skip(self) -> bool:
        return CONFIG.gold_point_card_plus.skip_amazon_row and self.store.is_amazon


class GoldPointCardPlus201912RowFactory(InputRowFactory[GoldPointCardPlus201912RowData, GoldPointCardPlus201912Row]):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance."""
    def create(
            self, file_csv_convert_id: FileCsvConvertId, input_row_data: GoldPointCardPlus201912RowData
    ) -> GoldPointCardPlus201912Row:
        return GoldPointCardPlus201912Row(file_csv_convert_id, input_row_data)
