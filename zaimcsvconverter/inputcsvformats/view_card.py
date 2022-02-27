"""This module implements row model of VIEW CARD CSV."""
from datetime import datetime
import re

from pydantic.dataclasses import dataclass as pydantic_dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.inputcsvformats.customdatatypes.string_with_comma_to_int import StrictStringWithCommaToInt
from zaimcsvconverter.inputcsvformats import InputRowFactory, InputStoreRow, InputStoreRowData


@pydantic_dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class ViewCardRowData(InputStoreRowData):
    """This class implements data class for wrapping list of VIEW CARD CSV row model."""

    used_date: StringToDateTime
    used_place: str
    used_amount: str
    refund_amount: str
    billing_amount: str
    number_of_division: str
    current_time_of_division: str
    billing_amount_current_time: StrictStringWithCommaToInt
    local_currency_amount: str
    currency_abbreviation: str
    exchange_rate: str

    @property
    def date(self) -> datetime:
        return self.used_date

    @property
    def store_name(self) -> str:
        return self.used_place

    @property
    def is_suica(self) -> bool:
        """This property returns whether this store is Amazon.co.jp or not."""
        return bool(re.search(r"　オートチャージ$", self.used_place))


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
