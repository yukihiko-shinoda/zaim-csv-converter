"""This module implements model of input CSV."""
from typing import Generic, List

from tests.testlibraries.csv_types import CSVWriter
from zaimcsvconverter.account import AccountContext
from zaimcsvconverter.csvconverter.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.datasources.data_source import DataSource
from zaimcsvconverter.errorhandling.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.exceptions import InvalidRecordError, SkipRecord
from zaimcsvconverter.inputcsvformats import TypeVarInputRow, TypeVarInputRowData
from zaimcsvconverter.inputtooutput.record_converter import RecordConverter


class InputData(Generic[TypeVarInputRowData, TypeVarInputRow]):
    """This class implements model of input CSV."""

    def __init__(self, datasource: DataSource, account_context: AccountContext[TypeVarInputRowData, TypeVarInputRow]):
        self.account_context = account_context
        self.record_processor = CsvRecordProcessor(self.account_context)
        self.record_converter = RecordConverter(self.account_context.zaim_row_converter_factory)
        self.data_source = datasource
        self.undefined_content_error_handler: UndefinedContentErrorHandler = UndefinedContentErrorHandler()

    def export_as_zaim_csv(self, writer_zaim: CSVWriter) -> None:
        """This method convert this csv into Zaim format CSV."""
        for list_input_row_standard_type_value in self.data_source:
            self._process_record(list_input_row_standard_type_value, writer_zaim)
        self.data_source.raise_error_if_invalid()

    def _process_record(self, list_input_row_standard_type_value: List[str], writer_zaim: CSVWriter) -> None:
        try:
            input_record = self.record_processor.execute(list_input_row_standard_type_value)
        except InvalidRecordError as exc:
            self.data_source.mark_current_record_as_error(exc.list_error)
            self.undefined_content_error_handler.extend(exc.undefined_content_error_handler)
            return
        except SkipRecord:
            return
        zaim_row = self.record_converter.convert(input_record)
        writer_zaim.writerow(zaim_row.convert_to_list())
