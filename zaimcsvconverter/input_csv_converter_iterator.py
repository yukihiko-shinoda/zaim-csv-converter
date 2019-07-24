"""This module implements iterating steps from input_csv_converter."""
import csv
from pathlib import Path
from typing import List

from zaimcsvconverter.error_handler import ErrorHandler
from zaimcsvconverter.input_csv_converter import InputCsvConverter


class InputCsvConverterIterator:
    """This class implements iterating steps from input_csv_converter."""
    FILE_NAME_ERROR = 'error.csv'

    def __init__(self, directory_csv_input: Path, directory_csv_output: Path):
        self.directory_csv_input = directory_csv_input
        self.directory_csv_output = directory_csv_output

    def execute(self) -> None:
        """This method executes all CSV converters."""
        list_csv_converter: List[InputCsvConverter] = []
        for path in self.directory_csv_input.glob('*.csv'):
            list_csv_converter.append(InputCsvConverter(path, self.directory_csv_output))
        error_handler = ErrorHandler()
        for csv_converter in list_csv_converter:
            try:
                csv_converter.execute()
            except KeyError:
                error_handler.extend(csv_converter.error_handler)
                continue
        if error_handler.is_presented:
            error_handler.uniquify()
            with (self.directory_csv_output / self.FILE_NAME_ERROR).open(
                    'w', encoding='UTF-8', newline='\n'
            ) as file_error:
                writer_error = csv.writer(file_error)
                for error_row in error_handler:
                    writer_error.writerow(error_row)
            raise KeyError(f'Undefined store name in convert table CSV exists. Please check {self.FILE_NAME_ERROR}.')
