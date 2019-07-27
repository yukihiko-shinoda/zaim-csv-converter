"""This module implements invalid input CSV handler."""
from typing import List, Generator, Union

from zaimcsvconverter.csv_exporter import CsvExporter
from zaimcsvconverter.error_handler import UndefinedContentErrorHandler, FileNameError
from zaimcsvconverter.input_csv import InputCsv


class InvalidInputCsvHandler:
    """This class implements handler of invalid input CSV."""
    def __init__(self):
        self.list_invalid_input_csv: List[InputCsv] = []
        self.undefined_content_error_handler: UndefinedContentErrorHandler = UndefinedContentErrorHandler()

    def __iter__(self) -> Generator[List[Union[int, str]], None, None]:
        for input_csv in self.list_invalid_input_csv:
            if input_csv.invalid_header_error is not None:
                yield [input_csv.path_to_file.name, '', str(input_csv.invalid_header_error)]
            for index, list_error in input_csv.dictionary_invalid_row.items():
                for error in list_error:
                    yield [input_csv.path_to_file.name, index, str(error)]

    def append(self, input_csv: InputCsv):
        """This method appends argument as invalid CSV."""
        self.list_invalid_input_csv.append(input_csv)
        self.undefined_content_error_handler.extend(input_csv.undefined_content_error_handler)

    @property
    def is_presented(self):
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return bool(self.list_invalid_input_csv)

    def export_to_csv(self, directory_csv_output):
        """This method exports invalid input CSV errors into CSV."""
        csv_exporter = CsvExporter(directory_csv_output)
        csv_exporter.export(self, FileNameError.INVALID_ROW.value)
        if self.undefined_content_error_handler.is_presented:
            csv_exporter.export(self.undefined_content_error_handler, FileNameError.UNDEFINED_CONTENT.value)

    @property
    def message(self):
        """This property returns error message."""
        message = ('Some invalid input CSV file exists. '
                   f'Please check {FileNameError.INVALID_ROW.value}')
        if self.undefined_content_error_handler.is_presented:
            message = message + f' and {FileNameError.UNDEFINED_CONTENT.value}'
        return f'{message}.'
