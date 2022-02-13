"""This module implements row model of GOLD POINT CARD+ CSV version 201912."""
from dataclasses import dataclass
from datetime import datetime
import re

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats import InputRowFactory, InputStoreRow, InputStoreRowData


@dataclass
class ViewCardRowData(InputStoreRowData):
    """This class implements data class for wrapping list of VIEW CARD CSV row model."""

    # Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
    _used_date: str
    _used_place: str
    _used_amount: str
    _refund_amount: str
    _billing_amount: str
    _number_of_division: str
    _current_time_of_division: str
    _billing_amount_current_time: str
    _local_currency_amount: str
    _currency_abbreviation: str
    _exchange_rate: str

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._used_date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        return self._used_place

    @property
    def billing_amount_current_time(self) -> int:
        return int(self._billing_amount_current_time.replace(",", ""))

    @property
    def is_suica(self) -> bool:
        """This property returns whether this store is Amazon.co.jp or not."""
        return bool(re.search(r"　オートチャージ$", self._used_place))

    @property
    def validate(self) -> bool:
        self.stock_error(lambda: self.date, f"Invalid used date. Used date = {self._used_date}")
        self.stock_error(
            lambda: self.billing_amount_current_time,
            f"Invalid billing amount of current time. "
            f"Billing amount of current time = {self._billing_amount_current_time}",
        )
        return super().validate


class ViewCardRow(InputStoreRow[ViewCardRowData]):
    """This class implements row model of GOLD POINT CARD+ CSV."""

    def __init__(self, row_data: ViewCardRowData):
        super().__init__(row_data, FileCsvConvert.VIEW_CARD.value)
        self.billing_amount_current_time: int = row_data.billing_amount_current_time
        self._is_suica: bool = row_data.is_suica

    @property
    def is_row_to_skip(self) -> bool:
        return CONFIG.view_card.skip_suica_row and self._is_suica


class ViewCardRowFactory(InputRowFactory[ViewCardRowData, ViewCardRow]):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: ViewCardRowData) -> ViewCardRow:  # type: ignore
        return ViewCardRow(input_row_data)
