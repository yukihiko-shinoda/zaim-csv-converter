"""This module implements row model of VIEW CARD CSV."""

from typing import Any

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csv.data.view_card import ViewCardRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputRow, InputStoreRow


class ViewCardRow(InputRow[ViewCardRowData]):
    def __init__(self, row_data: ViewCardRowData, *args: Any, **kwargs: Any) -> None:
        super().__init__(row_data, *args, **kwargs)
        self.billing_amount_current_time: int = row_data.billing_amount_current_time


class ViewCardNotStoreRow(ViewCardRow):
    """This class implements row model of GOLD POINT CARD+ CSV."""

    @property
    def is_row_to_skip(self) -> bool:
        return CONFIG.view_card.skip_suica_row


class ViewCardStoreRow(ViewCardRow, InputStoreRow[ViewCardRowData]):
    """This class implements row model of GOLD POINT CARD+ CSV."""

    def __init__(self, row_data: ViewCardRowData) -> None:
        super().__init__(row_data, FileCsvConvert.VIEW_CARD.value)

    @property
    def is_row_to_skip(self) -> bool:
        return False
