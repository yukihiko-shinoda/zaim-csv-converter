"""This module implements row model of GOLD POINT CARD+ CSV."""
from datetime import datetime

from pydantic.dataclasses import dataclass as pydantic_dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.inputcsvformats import InputRowFactory, InputStoreRow, InputStoreRowData


@pydantic_dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class GoldPointCardPlusRowData(InputStoreRowData):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV row model."""

    used_date: StringToDateTime
    used_store: str
    used_card: str
    payment_kind: str
    number_of_division: str
    scheduled_payment_month: str
    used_amount: int
    unknown_1: str
    unknown_2: str
    unknown_3: str
    unknown_4: str
    unknown_5: str
    unknown_6: str

    @property
    def date(self) -> datetime:
        return self.used_date

    @property
    def store_name(self) -> str:
        return self.used_store


class GoldPointCardPlusRow(InputStoreRow[GoldPointCardPlusRowData]):
    """This class implements row model of GOLD POINT CARD+ CSV."""

    def __init__(self, row_data: GoldPointCardPlusRowData):
        super().__init__(row_data, FileCsvConvert.GOLD_POINT_CARD_PLUS.value)
        self.used_amount: int = row_data.used_amount

    @property
    def is_row_to_skip(self) -> bool:
        return (
            CONFIG.gold_point_card_plus.skip_amazon_row
            and self.store.is_amazon
            or CONFIG.gold_point_card_plus.skip_pay_pal_row
            and self.store.is_pay_pal
        ) and self.used_amount >= 0


class GoldPointCardPlusRowFactory(InputRowFactory[GoldPointCardPlusRowData, GoldPointCardPlusRow]):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: GoldPointCardPlusRowData) -> GoldPointCardPlusRow:  # type: ignore
        return GoldPointCardPlusRow(input_row_data)
