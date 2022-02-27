"""This module implements row model of GOLD POINT CARD+ CSV version 201912."""
from dataclasses import dataclass
from datetime import datetime

from pydantic.dataclasses import dataclass as pydantic_dataclass
from sqlalchemy.orm.exc import NoResultFound

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats import AbstractPydantic, InputRowFactory, InputStoreRow, InputStoreRowData
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_datetime import StringToDateTime


@pydantic_dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class GoldPointCardPlus201912RowDataPydantic(AbstractPydantic):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV version 201912 row model."""

    used_date: StringToDateTime
    used_store: str
    used_amount: str
    number_of_division: str
    current_time_of_division: str
    payed_amount: int
    others: str


@dataclass
class GoldPointCardPlus201912RowData(InputStoreRowData[GoldPointCardPlus201912RowDataPydantic]):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV version 201912 row model."""

    _used_date: str
    _used_store: str
    _used_amount: str
    _number_of_division: str
    _current_time_of_division: str
    _payed_amount: str
    others: str

    def create_pydantic(self) -> GoldPointCardPlus201912RowDataPydantic:
        return GoldPointCardPlus201912RowDataPydantic(
            # Reason: Maybe, there are no way to specify type before converted by pydantic
            self._used_date,  # type: ignore
            self._used_store,
            self._used_amount,
            self._number_of_division,
            self._current_time_of_division,
            self._payed_amount,  # type: ignore
            self.others,
        )

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._used_date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        return self.pydantic.used_store

    @property
    def payed_amount(self) -> int:
        return self.pydantic.payed_amount

    @property
    def validate(self) -> bool:
        return super().validate


class GoldPointCardPlus201912Row(InputStoreRow[GoldPointCardPlus201912RowData]):
    """This class implements row model of GOLD POINT CARD+ CSV."""

    OTHERS_RETURN = "返品"

    def __init__(self, row_data: GoldPointCardPlus201912RowData):
        super().__init__(row_data, FileCsvConvert.GOLD_POINT_CARD_PLUS.value)
        self.payed_amount: int = row_data.payed_amount
        self.others: str = row_data.others

    @property
    def is_row_to_skip(self) -> bool:
        try:
            store = self.store
        except NoResultFound:
            return False
        return CONFIG.gold_point_card_plus.skip_amazon_row and store.is_amazon and self.others != self.OTHERS_RETURN


class GoldPointCardPlus201912RowFactory(InputRowFactory[GoldPointCardPlus201912RowData, GoldPointCardPlus201912Row]):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: GoldPointCardPlus201912RowData) -> GoldPointCardPlus201912Row:  # type: ignore
        return GoldPointCardPlus201912Row(input_row_data)
