"""This module implements row model of GOLD POINT CARD+ CSV version 201912."""
import re
from datetime import datetime
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats import InputStoreRowData, InputStoreRow, InputRowFactory
from zaimcsvconverter.models import FileCsvConvertId


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
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return int(self._billing_amount_current_time.replace(',', ''))

    @property
    def is_suica(self) -> bool:
        """This property returns whether this store is Amazon.co.jp or not."""
        return bool(re.search(r'　オートチャージ$', self._used_place))

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.date,
            f'Invalid used date. Used date = {self._used_date}'
        )
        self.stock_error(
            lambda: self.billing_amount_current_time,
            f'Invalid billing amount of current time. '
            f'Billing amount of current time = {self._billing_amount_current_time}'
        )
        return super().validate


class ViewCardRow(InputStoreRow):
    """This class implements row model of GOLD POINT CARD+ CSV."""
    def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: ViewCardRowData):
        super().__init__(file_csv_convert_id, row_data)
        self.billing_amount_current_time: int = row_data.billing_amount_current_time
        self._is_suica: bool = row_data.is_suica

    @property
    def is_row_to_skip(self) -> bool:
        return CONFIG.view_card.skip_suica_row and self._is_suica


class ViewCardRowFactory(InputRowFactory[ViewCardRowData, ViewCardRow]):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance."""
    def create(
            self, file_csv_convert_id: FileCsvConvertId, input_row_data: ViewCardRowData
    ) -> ViewCardRow:
        return ViewCardRow(file_csv_convert_id, input_row_data)