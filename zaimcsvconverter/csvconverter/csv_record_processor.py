"""This module implements convert steps of input CSV row."""
from typing import cast, Generic, List, Optional

from pydantic import ValidationError
from returns.primitives.hkt import Kind1

from zaimcsvconverter.account import AccountContext
from zaimcsvconverter.errorhandling.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.exceptions import InvalidCellError, InvalidRecordError, SkipRecord
from zaimcsvconverter.inputcsvformats import (
    InputContentRow,
    InputRow,
    InputRowData,
    TypeVarInputRow,
    TypeVarInputRowData,
)


class CsvRecordProcessor(Generic[TypeVarInputRowData, TypeVarInputRow]):
    """This class implements convert steps of input CSV row."""

    def __init__(self, account_context: AccountContext[TypeVarInputRowData, TypeVarInputRow]):
        self.input_row_data_class = account_context.input_row_data_class
        self.input_row_factory = account_context.input_row_factory

    def execute(self, list_input_row_standard_type_value: List[str]) -> Kind1[TypeVarInputRow, TypeVarInputRowData]:
        """This method executes convert steps of input CSV row."""
        try:
            input_record_data = self.input_row_data_class(*list_input_row_standard_type_value)
        except ValidationError as exc:
            raise InvalidRecordError(
                [InvalidCellError(f"Invalid {error['loc'][0]}, {error['msg']}") for error in exc.errors()]
            ) from exc
        input_record = self.create_input_row_instance(input_record_data)
        dekinded_input_record = cast(InputRow[InputRowData], input_record)
        if dekinded_input_record.is_row_to_skip:
            raise SkipRecord()
        if dekinded_input_record.validate:
            raise InvalidRecordError(
                dekinded_input_record.list_error,
                undefined_content_error_handler=self.create_undefined_content_error_handler(input_record),
            )
        return input_record

    @staticmethod
    def create_undefined_content_error_handler(
        input_row: Kind1[InputRow[InputRowData], InputRowData]
    ) -> Optional[UndefinedContentErrorHandler]:
        """To simplify instantiate process."""
        dekinded_input_row = cast(InputRow[InputRowData], input_row)
        if not isinstance(dekinded_input_row, InputContentRow):
            return None
        undefined_content_error_handler = UndefinedContentErrorHandler()
        undefined_content_error_handler.extend_list(dekinded_input_row.get_report_undefined_content_error())
        return undefined_content_error_handler

    def create_input_row_instance(
        self, input_row_data: TypeVarInputRowData
    ) -> Kind1[TypeVarInputRow, TypeVarInputRowData]:
        """This method creates input row instance by input row data instance."""
        return self.input_row_factory.create(input_row_data)
