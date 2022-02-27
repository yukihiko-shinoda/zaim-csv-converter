"""This module implements row model of SF Card Viewer CSV."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Callable

from pydantic.dataclasses import dataclass as pydantic_dataclass

from zaimcsvconverter.config import SFCardViewerConfig
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.inputcsvformats import InputRow, InputRowFactory, InputStoreRow, InputStoreRowData


# Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
class Note(str, Enum):
    """This class implements constant of note in SF Card Viewer CSV."""

    EMPTY = ""
    SALES_GOODS = "物販"
    AUTO_CHARGE = "ｵｰﾄﾁｬｰｼﾞ"
    EXIT_BY_WINDOW = "窓出"
    BUS_TRAM = "ﾊﾞｽ/路面等"


@pydantic_dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class SFCardViewerRowData(InputStoreRowData):
    """This class implements data class for wrapping list of SF Card Viewer CSV row model."""

    used_date: StringToDateTime
    is_commuter_pass_enter: str
    railway_company_name_enter: str
    station_name_enter: str
    is_commuter_pass_exit: str
    railway_company_name_exit: str
    station_name_exit: str
    used_amount: int
    balance: str
    note: Note

    @property
    def date(self) -> datetime:
        return self.used_date

    @property
    def store_name(self) -> str:
        return self.station_name_enter if self.is_auto_charge else self.station_name_exit

    @property
    def is_auto_charge(self) -> bool:
        """This property returns whether this row is auto charge or not."""
        return self.note == Note.AUTO_CHARGE


# pylint: disable=too-many-instance-attributes
class SFCardViewerRow(InputRow[SFCardViewerRowData]):
    """This class implements row model of SF Card Viewer CSV."""

    def __init__(
        self, row_data: SFCardViewerRowData, account_config: SFCardViewerConfig, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(row_data, *args, **kwargs)
        self.used_amount: int = row_data.used_amount
        self.note = row_data.note
        self._account_config: SFCardViewerConfig = account_config

    @property
    def is_row_to_skip(self) -> bool:
        return self.is_sales_goods and self._account_config.skip_sales_goods_row

    @property
    def is_transportation(self) -> bool:
        return self.note == Note.EMPTY

    @property
    def is_sales_goods(self) -> bool:
        return self.note == Note.SALES_GOODS

    @property
    def is_auto_charge(self) -> bool:
        return self.note == Note.AUTO_CHARGE

    @property
    def is_exit_by_window(self) -> bool:
        return self.note == Note.EXIT_BY_WINDOW

    @property
    def is_bus_tram(self) -> bool:
        return self.note == Note.BUS_TRAM


class SFCardViewerEnterRow(SFCardViewerRow, InputStoreRow[SFCardViewerRowData]):
    """This class implements enter station row model of SF Card Viewer CSV."""

    def __init__(self, row_data: SFCardViewerRowData, account_config: SFCardViewerConfig):
        super().__init__(row_data, account_config, FileCsvConvert.SF_CARD_VIEWER.value)
        self.railway_company_name_enter: str = row_data.railway_company_name_enter
        self.station_name_enter: str = row_data.station_name_enter


class SFCardViewerEnterExitRow(SFCardViewerEnterRow):
    """This class implements enter and exit station row model of SF Card Viewer CSV."""

    def __init__(self, row_data: SFCardViewerRowData, account_config: SFCardViewerConfig):
        super().__init__(row_data, account_config)
        self.railway_company_name_exit: str = row_data.railway_company_name_exit

    @property
    def is_row_to_skip(self) -> bool:
        return (
            self.is_exit_by_window
            and self.used_amount == 0
            and self.railway_company_name_enter == self.railway_company_name_exit
            and self.station_name_enter == self.store.name
        )


class SFCardViewerRowFactory(InputRowFactory[SFCardViewerRowData, SFCardViewerRow]):
    """This class implements factory to create WAON CSV row instance."""

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
