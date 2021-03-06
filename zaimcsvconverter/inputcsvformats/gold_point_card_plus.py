"""This module implements row model of GOLD POINT CARD+ CSV."""
from dataclasses import dataclass
from datetime import datetime

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats import InputRowFactory, InputStoreRow, InputStoreRowData


@dataclass
class GoldPointCardPlusRowData(InputStoreRowData):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV row model."""

    # Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
    _used_date: str
    _used_store: str
    used_card: str
    payment_kind: str
    number_of_division: str
    scheduled_payment_month: str
    _used_amount: str
    unknown_1: str
    unknown_2: str
    unknown_3: str
    unknown_4: str
    unknown_5: str
    unknown_6: str

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._used_date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        return self._used_store

    @property
    def used_amount(self) -> int:
        return int(self._used_amount)

    @property
    def validate(self) -> bool:
        self.stock_error(lambda: self.date, f"Invalid used date. Used date = {self._used_date}")
        self.stock_error(lambda: self.used_amount, f"Invalid used amount. Used amount = {self._used_amount}")
        return super().validate


class GoldPointCardPlusRow(InputStoreRow):
    """This class implements row model of GOLD POINT CARD+ CSV."""

    def __init__(self, row_data: GoldPointCardPlusRowData):
        super().__init__(row_data, FileCsvConvert.GOLD_POINT_CARD_PLUS.value)
        self.used_amount: int = row_data.used_amount

    @property
    def is_row_to_skip(self) -> bool:
        return (
            CONFIG.gold_point_card_plus.skip_amazon_row
            and self.store.is_amazon
            or CONFIG.gold_point_card_plus.skip_pay_pal_row
            and self.store.is_pay_pal
        ) and self.used_amount >= 0


class GoldPointCardPlusRowFactory(InputRowFactory[GoldPointCardPlusRowData, GoldPointCardPlusRow]):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance."""

    def create(self, input_row_data: GoldPointCardPlusRowData) -> GoldPointCardPlusRow:
        return GoldPointCardPlusRow(input_row_data)
