"""This module implements row model of VIEW CARD CSV."""
from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csv.data.view_card import ViewCardRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputRow, InputStoreRow


class ViewCardNotStoreRow(InputRow[ViewCardRowData]):
    """This class implements row model of GOLD POINT CARD+ CSV."""

    def __init__(self, row_data: ViewCardRowData) -> None:
        super().__init__(row_data)
        self.billing_amount_current_time: int = row_data.billing_amount_current_time

    @property
    def is_row_to_skip(self) -> bool:
        return CONFIG.view_card.skip_suica_row


class ViewCardStoreRow(InputStoreRow[ViewCardRowData]):
    """This class implements row model of GOLD POINT CARD+ CSV."""

    def __init__(self, row_data: ViewCardRowData) -> None:
        super().__init__(row_data, FileCsvConvert.VIEW_CARD.value)
        self.billing_amount_current_time: int = row_data.billing_amount_current_time

    @property
    def is_row_to_skip(self) -> bool:
        return False
