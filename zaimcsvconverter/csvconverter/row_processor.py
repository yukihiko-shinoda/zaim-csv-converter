"""This module implements convert steps of input CSV row."""
from typing import Generic, List, cast

from godslayer.exceptions import InvalidRecordError
from returns.primitives.hkt import Kind1

from zaimcsvconverter.account import AccountContext
from zaimcsvconverter.errorhandling.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.exceptions import SkipRow
from zaimcsvconverter.inputcsvformats import (
    AbstractPydantic,
    InputContentRow,
    InputRow,
    InputRowData,
    TypeVarInputRow,
    TypeVarInputRowData,
)
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class RecordProcessor(Generic[TypeVarInputRowData, TypeVarInputRow]):
    """This class implements convert steps of input CSV row."""

    def __init__(self, account_context: AccountContext[TypeVarInputRowData, TypeVarInputRow]):
        self._account_context = account_context
        self.list_error: List[InvalidRecordError] = []
        self.undefined_content_error_handler: UndefinedContentErrorHandler = UndefinedContentErrorHandler()

    def execute(self, list_input_row_standard_type_value: List[str]) -> ZaimRow:
        """This method executes convert steps of input CSV row."""
        input_row_data = self._account_context.create_input_row_data_instance(list_input_row_standard_type_value)
        if input_row_data.validate:
            self.list_error = input_row_data.list_error
            raise InvalidRecordError()
        input_row = self._account_context.create_input_row_instance(input_row_data)
        dekinded_input_row = cast(InputRow[InputRowData[AbstractPydantic]], input_row)
        if dekinded_input_row.is_row_to_skip:
            raise SkipRow()
        if dekinded_input_row.validate:
            self._stock_row_error(input_row)
            raise InvalidRecordError()
        return self._account_context.convert_input_row_to_zaim_row(input_row)

    def _stock_row_error(
        self, input_row: Kind1[InputRow[InputRowData[AbstractPydantic]], InputRowData[AbstractPydantic]]
    ) -> None:
        self.list_error = input_row.list_error
        if not isinstance(input_row, InputContentRow):
            return
        self.undefined_content_error_handler.extend_list(input_row.get_report_undefined_content_error())
