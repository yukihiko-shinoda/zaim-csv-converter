"""This module implements model of input CSV."""
import csv
from pathlib import Path
from typing import Dict, Optional, List

from zaimcsvconverter.account import Account
from zaimcsvconverter.error_collector import SingleErrorCollector
from zaimcsvconverter.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.exceptions import InvalidHeaderError, InvalidInputCsvError, InvalidRowError
from zaimcsvconverter.inputcsvformats import InputRowData, InputRow


class InputCsv:
    """This class implements model of input CSV."""
    def __init__(self, path_to_file):
        self.path_to_file: Path = path_to_file
        self._account = Account.create_by_path_csv_input(path_to_file)
        self.undefined_content_error_handler: UndefinedContentErrorHandler = UndefinedContentErrorHandler()
        self.invalid_header_error: Optional[InvalidHeaderError] = None
        self.dictionary_invalid_row: Dict[int, List[InvalidRowError]] = {}

    @property
    def is_invalid(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.invalid_header_error is not None or bool(self.dictionary_invalid_row)

    def covert_to_zaim(self, writer_zaim) -> None:
        """This method convert this csv into Zaim format CSV."""
        account_context = self._account.value
        with self.path_to_file.open('r', encoding=account_context.encode) as file_input:
            reader_input = csv.reader(file_input)
            if account_context.csv_header:
                self._skip_header(reader_input)
            for index, list_input_row_standard_type_value in enumerate(reader_input):
                self._process_row(index, list_input_row_standard_type_value, writer_zaim)
        if self.is_invalid:
            raise InvalidInputCsvError(
                f'Undefined store name in convert table CSV exists in {self.path_to_file.name}.'
                + 'Please check property AccountCsvConverter.list_undefined_store.'
            )

    def _skip_header(self, reader_input):
        error_message = (f'{self.path_to_file.name} does not include header row.'
                         'Please confirm AccountConfig.csv_header. '
                         f'AccountConfig.csv_header = {self._account.value.csv_header}')
        error_collector = SingleErrorCollector(InvalidHeaderError, error_message)
        with error_collector:
            while reader_input.__next__() != self._account.value.csv_header:
                pass
        if error_collector.error is not None:
            self.invalid_header_error = error_collector.error
            raise InvalidInputCsvError(error_message) from error_collector.error

    def _process_row(self, index: int, list_input_row_standard_type_value: List[str], writer_zaim) -> None:
        input_row_data = self._account.create_input_row_data_instance(list_input_row_standard_type_value)
        if input_row_data.validate(self._account.value.id):
            self._stock_row_data_error(index, input_row_data)
            return
        input_row = self._account.create_input_row_instance(input_row_data)
        if input_row.validate:
            self._stock_row_error(index, input_row)
            return
        if input_row.is_row_to_skip:
            return
        converter = self._account.value.zaim_row_converter_selector.select(input_row)
        zaim_row = converter(input_row).convert()
        list_row_zaim = zaim_row.convert_to_list()
        writer_zaim.writerow(list_row_zaim)

    def _stock_row_data_error(self, index, input_row_data: InputRowData):
        self.dictionary_invalid_row[index] = input_row_data.list_error
        if input_row_data.undefined_content_error is None:
            return
        self.undefined_content_error_handler.append(self._account.value.file_name_csv_convert, input_row_data)

    def _stock_row_error(self, index, input_row: InputRow):
        self.dictionary_invalid_row[index] = input_row.list_error
