"""This module implements row model of SF Card Viewer CSV."""
from __future__ import annotations

from typing import Any

from zaimcsvconverter.config import SFCardViewerConfig
from zaimcsvconverter.data.sf_card_viewer import Note
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csv.data.sf_card_viewer import SFCardViewerRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputRow, InputStoreRow


# pylint: disable=too-many-instance-attributes
class SFCardViewerRow(InputRow[SFCardViewerRowData]):
    """This class implements row model of SF Card Viewer CSV."""

    def __init__(
        self, row_data: SFCardViewerRowData, account_config: SFCardViewerConfig, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(row_data, *args, **kwargs)
        self.used_amount = row_data.used_amount
        self.note = row_data.note
        self._account_config = account_config

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


# Specification requires. pylint: disable=too-many-ancestors
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
