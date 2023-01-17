"""This module implements row model of GOLD POINT CARD+ CSV version 201912."""
from sqlalchemy.orm.exc import NoResultFound

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csv.data.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912RowData,
)
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputStoreRow


class GoldPointCardPlus201912Row(InputStoreRow[GoldPointCardPlus201912RowData]):
    """This class implements row model of GOLD POINT CARD+ CSV."""

    OTHERS_RETURN = "返品"

    def __init__(self, row_data: GoldPointCardPlus201912RowData):
        super().__init__(row_data, FileCsvConvert.GOLD_POINT_CARD_PLUS.value)
        self.payed_amount: int = row_data.payed_amount
        self.others: str = row_data.others

    @property
    def is_row_to_skip(self) -> bool:
        return self.is_amazon_row_to_skip or self.is_pay_pal_row_to_skip or self.is_kyash_row_to_skip

    @property
    def is_amazon_row_to_skip(self) -> bool:
        try:
            store = self.store
        except NoResultFound:
            return False
        return CONFIG.gold_point_card_plus.skip_amazon_row and store.is_amazon and self.others != self.OTHERS_RETURN

    @property
    def is_pay_pal_row_to_skip(self) -> bool:
        return CONFIG.gold_point_card_plus.skip_pay_pal_row and self.store.is_pay_pal

    @property
    def is_kyash_row_to_skip(self) -> bool:
        return CONFIG.gold_point_card_plus.skip_kyash_row and self.store.is_kyash
