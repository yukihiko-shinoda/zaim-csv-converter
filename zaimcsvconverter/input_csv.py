"""This module implements model of input CSV."""
from typing import List

from godslayer.exceptions import InvalidRecordError

from tests.testlibraries.csv_types import CSVWriter
from zaimcsvconverter.account import Account
from zaimcsvconverter.datasources.data_source import DataSource
from zaimcsvconverter.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.exceptions import SkipRow
from zaimcsvconverter.row_processor import RecordProcessor


class InputData:
    """This class implements model of input CSV."""

    def __init__(self, datasource: DataSource, account: Account):
        self.account = account
        self.data_source = datasource
        self.undefined_content_error_handler: UndefinedContentErrorHandler = UndefinedContentErrorHandler()

    def export_as_zaim_csv(self, writer_zaim: CSVWriter) -> None:
        """This method convert this csv into Zaim format CSV."""
        for list_input_row_standard_type_value in self.data_source:
            self._process_record(list_input_row_standard_type_value, writer_zaim)
        self.data_source.raise_error_if_invalid()

    def _process_record(self, list_input_row_standard_type_value: List[str], writer_zaim: CSVWriter) -> None:
        record_processor = RecordProcessor(self.account)
        try:
            zaim_row = record_processor.execute(list_input_row_standard_type_value)
        except InvalidRecordError:
            self.data_source.mark_current_record_as_error(record_processor.list_error)
            self.undefined_content_error_handler.extend(record_processor.undefined_content_error_handler)
            return
        except SkipRow:
            return
        writer_zaim.writerow(zaim_row.convert_to_list())
