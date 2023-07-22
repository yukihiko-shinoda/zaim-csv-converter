"""This module implements row model of Mobile Suica CSV."""
from __future__ import annotations

from typing import Any, TYPE_CHECKING

from zaimcsvconverter.data.mobile_suica import Kind1, Kind2
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csv.data.mobile_suica import MobileSuicaRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputRow, InputStoreRow

if TYPE_CHECKING:
    from zaimcsvconverter.config import SFCardViewerConfig


# pylint: disable=too-many-instance-attributes
class MobileSuicaRow(InputRow[MobileSuicaRowData]):
    """This class implements row model of Mobile Suica CSV."""

    def __init__(
        self,
        row_data: MobileSuicaRowData,
        account_config: SFCardViewerConfig,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(row_data, *args, **kwargs)
        self.kind_1 = row_data.kind_1
        self.balance = row_data.balance
        self._deposit_used_amount = row_data.deposit_used_amount
        self._account_config = account_config

    @property
    def is_row_to_skip(self) -> bool:
        return self.is_sales_goods and self._account_config.skip_sales_goods_row

    @property
    def is_sales_goods(self) -> bool:
        return self.kind_1 == Kind1.SALES_GOODS

    @property
    def is_auto_charge(self) -> bool:
        return self.kind_1 == Kind1.AUTO_CHARGE

    @property
    def is_bus_tram(self) -> bool:
        return self.kind_1 == Kind1.BUS_ET_CETERA

    @property
    def deposit_used_amount(self) -> int:
        if self._deposit_used_amount is None:
            msg = "Deposit / Used Amount excluding in first row is empty."
            raise ValueError(msg)
        return self._deposit_used_amount

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.deposit_used_amount,
            "Deposit / Used Amount excluding in first row is required. "
            f"Deposit / Used Amount = {self._deposit_used_amount}",
        )
        return super().validate


class MobileSuicaStoreRow(MobileSuicaRow, InputStoreRow[MobileSuicaRowData]):
    """This class implements enter station row model of Mobile Suica CSV."""

    def __init__(self, row_data: MobileSuicaRowData, account_config: SFCardViewerConfig) -> None:
        super().__init__(row_data, account_config, FileCsvConvert.MOBILE_SUICA.value)


# Specification requires. pylint: disable=too-many-ancestors
class MobileSuicaFirstRow(MobileSuicaStoreRow):
    """This class implements enter station row model of Mobile Suica CSV."""

    @property
    def validate(self) -> bool:
        return super(MobileSuicaRow, self).validate


class MobileSuicaBusEtCeteraRow(MobileSuicaStoreRow):
    """This class implements bus or etc.

    row model of Mobile Suica CSV.
    """


# Specification requires. pylint: disable=too-many-ancestors
class MobileSuicaEnterExitRow(MobileSuicaStoreRow):
    """This class implements enter and exit station row model of Mobile Suica CSV."""

    def __init__(self, row_data: MobileSuicaRowData, account_config: SFCardViewerConfig) -> None:
        super().__init__(row_data, account_config)
        self.used_place_1 = row_data.used_place_1
        self.kind_2 = row_data.kind_2

    @property
    def is_row_to_skip(self) -> bool:
        return self.is_exit_by_window and self.deposit_used_amount == 0 and self.used_place_1 == self.store.name

    @property
    def is_transportation(self) -> bool:
        return self.kind_2 == Kind2.EXIT

    @property
    def is_exit_by_window(self) -> bool:
        return self.kind_2 == Kind2.EXIT_BY_WINDOW
