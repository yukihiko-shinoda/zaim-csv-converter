"""This module implements row model of SF Card Viewer CSV."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Callable
from dataclasses import dataclass

from zaimcsvconverter.inputcsvformats import InputStoreRowData, InputStoreRow, InputRowFactory, InputRow
from zaimcsvconverter.config import SFCardViewerConfig
from zaimcsvconverter.models import FileCsvConvertId


@dataclass
class SFCardViewerRowData(InputStoreRowData):
    """This class implements data class for wrapping list of SF Card Viewer CSV row model."""
    # Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
    class Note(Enum):
        """This class implements constant of note in SF Card Viewer CSV."""
        EMPTY = ''
        SALES_GOODS = '物販'
        AUTO_CHARGE = 'ｵｰﾄﾁｬｰｼﾞ'
        EXIT_BY_WINDOW = '窓出'
        BUS_TRAM = 'ﾊﾞｽ/路面等'

    _used_date: str
    is_commuter_pass_enter: str
    railway_company_name_enter: str
    station_name_enter: str
    is_commuter_pass_exit: str
    railway_company_name_exit: str
    _station_name_exit: str
    _used_amount: str
    balance: str
    _note: str

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._used_date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        return self.station_name_enter if self.is_auto_charge else self._station_name_exit

    @property
    def used_amount(self) -> int:
        return int(self._used_amount)

    @property
    def note(self) -> SFCardViewerRowData.Note:
        return SFCardViewerRowData.Note(self._note)

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.date,
            f'Invalid used date. Used date = {self._used_date}'
        )
        # This comment prevents pylint duplicate-code.
        self.stock_error(
            lambda: self.used_amount,
            f'Invalid used amount. Used amount = {self._used_amount}'
        )
        self.stock_error(
            lambda: self.note,
            f'Invalid note. Note = {self._note}'
        )
        return super().validate

    @property
    def is_auto_charge(self) -> bool:
        """This property returns whether this row is auto charge or not."""
        return self.note == SFCardViewerRowData.Note.AUTO_CHARGE


# pylint: disable=too-many-instance-attributes
class SFCardViewerRow(InputRow):
    """This class implements row model of SF Card Viewer CSV."""
    def __init__(self, row_data: SFCardViewerRowData, account_config: SFCardViewerConfig):
        super().__init__(FileCsvConvertId.SF_CARD_VIEWER, row_data)
        self.used_amount: int = row_data.used_amount
        self.note = row_data.note
        self._account_config: SFCardViewerConfig = account_config

    @property
    def is_row_to_skip(self) -> bool:
        return self.is_sales_goods and self._account_config.skip_sales_goods_row

    @property
    def is_transportation(self) -> bool:
        return self.note == SFCardViewerRowData.Note.EMPTY

    @property
    def is_sales_goods(self) -> bool:
        return self.note == SFCardViewerRowData.Note.SALES_GOODS

    @property
    def is_auto_charge(self) -> bool:
        return self.note == SFCardViewerRowData.Note.AUTO_CHARGE

    @property
    def is_exit_by_window(self) -> bool:
        return self.note == SFCardViewerRowData.Note.EXIT_BY_WINDOW

    @property
    def is_bus_tram(self) -> bool:
        return self.note == SFCardViewerRowData.Note.BUS_TRAM


class SFCardViewerEnterRow(SFCardViewerRow, InputStoreRow):
    """This class implements enter station row model of SF Card Viewer CSV."""
    def __init__(self, row_data: SFCardViewerRowData, account_config: SFCardViewerConfig):
        super().__init__(row_data, account_config)
        self.railway_company_name_enter: str = row_data.railway_company_name_enter
        self.station_name_enter: str = row_data.station_name_enter


class SFCardViewerEnterExitRow(SFCardViewerEnterRow):
    """This class implements enter and exit station row model of SF Card Viewer CSV."""
    def __init__(self, row_data: SFCardViewerRowData, account_config: SFCardViewerConfig):
        super().__init__(row_data, account_config)
        self.railway_company_name_exit: str = row_data.railway_company_name_exit

    @property
    def is_row_to_skip(self) -> bool:
        return self.is_exit_by_window and self.used_amount == 0 and \
               self.railway_company_name_enter == self.railway_company_name_exit and \
               self.station_name_enter == self.store.name


class SFCardViewerRowFactory(InputRowFactory[SFCardViewerRowData, SFCardViewerRow]):
    """This class implements factory to create WAON CSV row instance."""
    def __init__(self, account_config: Callable[[], SFCardViewerConfig]):
        self._account_config = account_config

    def create(self, input_row_data: SFCardViewerRowData) -> SFCardViewerRow:
        if input_row_data.note in (SFCardViewerRowData.Note.EMPTY, SFCardViewerRowData.Note.EXIT_BY_WINDOW):
            return SFCardViewerEnterExitRow(input_row_data, self._account_config())
        if input_row_data.note == SFCardViewerRowData.Note.AUTO_CHARGE:
            return SFCardViewerEnterRow(input_row_data, self._account_config())
        return SFCardViewerRow(input_row_data, self._account_config())
