"""This module implements row model of VIEW CARD CSV."""
from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csv.data.view_card import ViewCardRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputStoreRow


class ViewCardRow(InputStoreRow[ViewCardRowData]):
    """This class implements row model of GOLD POINT CARD+ CSV."""

    def __init__(self, row_data: ViewCardRowData):
        super().__init__(row_data, FileCsvConvert.VIEW_CARD.value)
        self.billing_amount_current_time: int = row_data.billing_amount_current_time
        self._is_suica: bool = row_data.is_suica

    @property
    def is_row_to_skip(self) -> bool:
        return CONFIG.view_card.skip_suica_row and self._is_suica
