"""This module implements row model of GOLD POINT CARD+ CSV."""

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csv.data.gold_point_card_plus import GoldPointCardPlusRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputStoreRow


class GoldPointCardPlusRow(InputStoreRow[GoldPointCardPlusRowData]):
    """This class implements row model of GOLD POINT CARD+ CSV."""

    def __init__(self, row_data: GoldPointCardPlusRowData) -> None:
        super().__init__(row_data, FileCsvConvert.GOLD_POINT_CARD_PLUS.value)
        self.used_amount: int = row_data.used_amount

    @property
    def is_row_to_skip(self) -> bool:
        return (
            CONFIG.gold_point_card_plus.skip_amazon_row
            and self.store.is_amazon
            or CONFIG.gold_point_card_plus.skip_pay_pal_row
            and self.store.is_pay_pal
            or CONFIG.gold_point_card_plus.skip_kyash_row
            and self.store.is_kyash
        ) and self.used_amount >= 0
