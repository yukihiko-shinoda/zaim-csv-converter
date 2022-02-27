"""This module implements convert steps of input CSV row."""
from typing import cast, Generic, List

from pydantic import ValidationError
from returns.primitives.hkt import Kind1

from zaimcsvconverter.account import AccountContext
from zaimcsvconverter.errorhandling.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.exceptions import InvalidCellError, InvalidRecordError, SkipRow
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
        self.list_error: List[InvalidCellError] = []
        self.undefined_content_error_handler: UndefinedContentErrorHandler = UndefinedContentErrorHandler()

    def execute(self, list_input_row_standard_type_value: List[str]) -> ZaimRow:
        """This method executes convert steps of input CSV row."""
        try:
            input_row_data = self._account_context.create_input_row_data_instance(list_input_row_standard_type_value)
        except ValidationError as exc:
            self.list_error.extend(
                [InvalidCellError(f"Invalid {error['loc'][0]}, {error['msg']}") for error in exc.errors()]
            )
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
        dekinded_input_row = cast(InputRow[InputRowData[AbstractPydantic]], input_row)
        self.list_error = dekinded_input_row.list_error
        if not isinstance(input_row, InputContentRow):
            return
        self.undefined_content_error_handler.extend_list(input_row.get_report_undefined_content_error())
