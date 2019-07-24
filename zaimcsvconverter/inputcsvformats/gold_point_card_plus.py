"""This module implements row model of GOLD POINT CARD+ CSV."""
from datetime import datetime
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats import InputStoreRowData, InputStoreRow, InputRowFactory
from zaimcsvconverter.models import Store, AccountId


@dataclass
class GoldPointCardPlusRowData(InputStoreRowData):
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV row model."""
    _used_date: str
    _used_store: str
    used_card: str
    payment_kind: str
    number_of_division: str
    scheduled_payment_month: str
    used_amount: str
    unknown_1: str
    unknown_2: str
    unknown_3: str
    unknown_4: str
    unknown_5: str
    unknown_6: str

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._used_date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        return self._used_store


class GoldPointCardPlusRow(InputStoreRow):
    """This class implements row model of GOLD POINT CARD+ CSV."""
    def __init__(self, account_id: AccountId, row_data: GoldPointCardPlusRowData):
        super().__init__(account_id, row_data)
        self.used_amount: int = int(row_data.used_amount)

    def is_row_to_skip(self, store: Store) -> bool:
        return CONFIG.gold_point_card_plus.skip_amazon_row and store.is_amazon


class GoldPointCardPlusRowFactory(InputRowFactory):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance."""
    def create(self, account_id: AccountId, row_data: GoldPointCardPlusRowData) -> GoldPointCardPlusRow:
        return GoldPointCardPlusRow(account_id, row_data)
