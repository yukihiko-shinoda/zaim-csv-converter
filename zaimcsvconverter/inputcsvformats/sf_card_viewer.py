"""This module implements row model of SF Card Viewer CSV."""
from datetime import datetime
from enum import Enum
from typing import Callable
from dataclasses import dataclass

from zaimcsvconverter.inputcsvformats import InputStoreRowData, InputStoreRow, InputRowFactory, ValidatedInputStoreRow
from zaimcsvconverter.config import SFCardViewerConfig
from zaimcsvconverter.models import Store, StoreRowData, AccountId


@dataclass
class SFCardViewerRowData(InputStoreRowData):
    """This class implements data class for wrapping list of SF Card Viewer CSV row model."""
    _used_date: str
    is_commuter_pass_enter: str
    railway_company_name_enter: str
    station_name_enter: str
    is_commuter_pass_exit: str
    railway_company_name_exit: str
    _station_name_exit: str
    used_amount: str
    balance: str
    note: str

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._used_date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        return self._station_name_exit


# pylint: disable=too-many-instance-attributes
class SFCardViewerRow(InputStoreRow):
    """This class implements row model of SF Card Viewer CSV."""
    class Note(Enum):
        """This class implements constant of note in SF Card Viewer CSV."""
        EMPTY = ''
        SALES_GOODS = '物販'
        AUTO_CHARGE = 'ｵｰﾄﾁｬｰｼﾞ'
        EXIT_BY_WINDOW = '窓出'
        BUS_TRAM = 'ﾊﾞｽ/路面等'

    def __init__(self, account_id: AccountId, row_data: SFCardViewerRowData, account_config: SFCardViewerConfig):
        super().__init__(account_id, row_data)
        self.railway_company_name_enter: str = row_data.railway_company_name_enter
        self.station_name_enter: str = row_data.station_name_enter
        self.railway_company_name_exit: str = row_data.railway_company_name_exit
        self.used_amount: int = int(row_data.used_amount)
        self._account_config: SFCardViewerConfig = account_config
        self.note = SFCardViewerRow.Note(row_data.note)
        if self.note == SFCardViewerRow.Note.BUS_TRAM:
            self._zaim_store: Store = Store(account_id, StoreRowData('', '', '交通', '電車'))

    def validate(self) -> ValidatedInputStoreRow:
        if self.note is None:
            raise ValueError(
                f'The value of "Note" has not been defined in this code. Note = {self.data.note}'
            )
        return super().validate()

    def is_row_to_skip(self, store: Store) -> bool:
        return self.note == SFCardViewerRow.Note.SALES_GOODS and self._account_config.skip_sales_goods_row or \
               self.note == SFCardViewerRow.Note.EXIT_BY_WINDOW and \
               self.used_amount == 0 and \
               self.railway_company_name_enter == self.railway_company_name_exit and \
               self.station_name_enter == store.name

    @property
    def is_transportation(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.note == SFCardViewerRow.Note.EMPTY

    @property
    def is_sales_goods(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.note == SFCardViewerRow.Note.SALES_GOODS

    @property
    def is_auto_charge(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.note == SFCardViewerRow.Note.AUTO_CHARGE

    @property
    def is_exit_by_window(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.note == SFCardViewerRow.Note.EXIT_BY_WINDOW

    @property
    def is_bus_tram(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.note == SFCardViewerRow.Note.BUS_TRAM


class SFCardViewerRowFactory(InputRowFactory):
    """This class implements factory to create WAON CSV row instance."""
    def __init__(self, account_config: Callable[[], SFCardViewerConfig]):
        self._account_config = account_config

    def create(self, account_id: AccountId, row_data: SFCardViewerRowData) -> SFCardViewerRow:
        return SFCardViewerRow(account_id, row_data, self._account_config())
