"""This module implements row model of VIEW CARD CSV."""
from dataclasses import dataclass
from datetime import datetime
import re

from pydantic.dataclasses import dataclass as pydantic_dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats import AbstractPydantic, InputRowFactory, InputStoreRow, InputStoreRowData
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.inputcsvformats.customdatatypes.string_with_comma_to_int import StrictStringWithCommaToInt


@pydantic_dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class ViewCardRowDataPydantic(AbstractPydantic):
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


@dataclass
class ViewCardRowData(InputStoreRowData[ViewCardRowDataPydantic]):
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

    def create_pydantic(self) -> ViewCardRowDataPydantic:
        return ViewCardRowDataPydantic(
            # Reason: Maybe, there are no way to specify type before converted by pydantic
            self._used_date,  # type: ignore
            self._used_place,
            self._used_amount,
            self._refund_amount,
            self._billing_amount,
            self._number_of_division,
            self._current_time_of_division,
            self._billing_amount_current_time,  # type: ignore
            self._local_currency_amount,
            self._currency_abbreviation,
            self._exchange_rate,
        )

    @property
    def date(self) -> datetime:
        return self.pydantic.used_date

    @property
    def store_name(self) -> str:
        return self.pydantic.used_place

    @property
    def billing_amount_current_time(self) -> int:
        return self.pydantic.billing_amount_current_time

    @property
    def is_suica(self) -> bool:
        """This property returns whether this store is Amazon.co.jp or not."""
        return bool(re.search(r"　オートチャージ$", self.pydantic.used_place))

    @property
    def validate(self) -> bool:
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
