"""This module implements convert steps of input CSV row."""
from typing import cast, Generic, Optional

from returns.primitives.hkt import Kind1

from zaimcsvconverter.errorhandling.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.exceptions import InvalidRecordError, SkipRecord
from zaimcsvconverter.inputtooutput.datasources.csv.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data import InputRowData, TypeVarInputRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputContentRow, InputRow, TypeVarInputRow


class CsvRecordProcessor(Generic[TypeVarInputRowData, TypeVarInputRow]):
    """This class implements convert steps of input CSV row."""

    def __init__(
        self,
        input_row_factory: InputRowFactory[TypeVarInputRowData, TypeVarInputRow],
    ) -> None:
        self.input_row_factory = input_row_factory

    def execute(self, input_record_data: TypeVarInputRowData) -> Kind1[TypeVarInputRow, TypeVarInputRowData]:
        """This method executes convert steps of input CSV row."""
        input_record = self.create_input_row_instance(input_record_data)
        dekinded_input_record = cast(InputRow[InputRowData], input_record)
        # Requires to validate before skip check process since skip check process checks store.
        if dekinded_input_record.validate:
            raise InvalidRecordError(
                dekinded_input_record.list_error,
                undefined_content_error_handler=self.create_undefined_content_error_handler(input_record),
            )
        if dekinded_input_record.is_row_to_skip:
            raise SkipRecord
        return input_record

    @staticmethod
    def create_undefined_content_error_handler(
        input_row: Kind1[InputRow[InputRowData], InputRowData],
    ) -> Optional[UndefinedContentErrorHandler]:
        """To simplify instantiate process."""
        dekinded_input_row = cast(InputRow[InputRowData], input_row)
        if not isinstance(dekinded_input_row, InputContentRow):
            return None
        undefined_content_error_handler = UndefinedContentErrorHandler()
        undefined_content_error_handler.extend_list(dekinded_input_row.get_report_undefined_content_error())
        return undefined_content_error_handler

    def create_input_row_instance(
        self,
        input_row_data: TypeVarInputRowData,
    ) -> Kind1[TypeVarInputRow, TypeVarInputRowData]:
        """This method creates input row instance by input row data instance."""
        return self.input_row_factory.create(input_row_data)
