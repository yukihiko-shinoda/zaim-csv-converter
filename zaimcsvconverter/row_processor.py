"""This module implements convert steps of input CSV row."""
from typing import List

from zaimcsvconverter.account import Account
from zaimcsvconverter.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.exceptions import InvalidRowError, SkipRow
from zaimcsvconverter.inputcsvformats import InputRowData, InputRow, InputStoreRow, InputItemRow
from zaimcsvconverter.zaim_row import ZaimRow


class RowProcessor:
    """This class implements convert steps of input CSV row."""
    def __init__(self, account: Account):
        self._account = account
        self.undefined_content_error_handler: UndefinedContentErrorHandler = UndefinedContentErrorHandler()
        self.list_error: List[InvalidRowError] = []

    def execute(self, list_input_row_standard_type_value: List[str]) -> ZaimRow:
        """This method executes convert steps of input CSV row."""
        input_row_data = self._account.create_input_row_data_instance(list_input_row_standard_type_value)
        if input_row_data.validate:
            self._stock_row_data_error(input_row_data)
            raise InvalidRowError()
        input_row = self._account.create_input_row_instance(input_row_data)
        if input_row.validate:
            self._stock_row_error(input_row)
            raise InvalidRowError()
        if input_row.is_row_to_skip:
            raise SkipRow()
        return self._account.convert_input_row_to_zaim_row(input_row)

    def _stock_row_data_error(self, input_row_data: InputRowData):
        self.list_error = input_row_data.list_error

    def _stock_row_error(self, input_row: InputRow):
        self.list_error = input_row.list_error
        if not isinstance(input_row, (InputStoreRow, InputItemRow)) or input_row.undefined_content_error is None:
            return
        self.undefined_content_error_handler.append(self._account.value.file_name_csv_convert, input_row)
        self.list_error.insert(0, input_row.undefined_content_error)
