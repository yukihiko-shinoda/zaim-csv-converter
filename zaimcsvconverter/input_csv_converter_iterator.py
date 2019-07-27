"""This module implements iterating steps from input_csv_converter."""
from pathlib import Path
from typing import List

from zaimcsvconverter.invalid_input_csv_handler import InvalidInputCsvHandler
from zaimcsvconverter.exceptions import InvalidInputCsvError
from zaimcsvconverter.input_csv_converter import InputCsvConverter


class InputCsvConverterIterator:
    """This class implements iterating steps from input_csv_converter."""

    def __init__(self, directory_csv_input: Path, directory_csv_output: Path):
        self.directory_csv_input = directory_csv_input
        self.directory_csv_output = directory_csv_output

    def execute(self) -> None:
        """This method executes all CSV converters."""
        invalid_input_csv_handler = InvalidInputCsvHandler()
        for csv_converter in self._initialize_list_csv_converter():
            try:
                csv_converter.execute()
            except InvalidInputCsvError:
                invalid_input_csv_handler.append(csv_converter.input_csv)
        if invalid_input_csv_handler.is_presented:
            invalid_input_csv_handler.export_to_csv(self.directory_csv_output)
            raise InvalidInputCsvError(invalid_input_csv_handler.message)

    def _initialize_list_csv_converter(self):
        list_csv_converter: List[InputCsvConverter] = []
        for path_csv_file in self.directory_csv_input.glob('*.csv'):
            list_csv_converter.append(InputCsvConverter(path_csv_file, self.directory_csv_output))
        return list_csv_converter
