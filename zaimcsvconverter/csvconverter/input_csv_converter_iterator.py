"""This module implements iterating steps from input_csv_converter."""
from pathlib import Path

from zaimcsvconverter.errorreporters.error_totalizer import ErrorTotalizer
from zaimcsvconverter.exceptions import SomeInvalidInputCsvError


class InputCsvConverterIterator:
    """This class implements iterating steps from input_csv_converter."""

    def __init__(self, directory_csv_input: Path, directory_csv_output: Path):
        self.directory_csv_input = directory_csv_input
        self.error_totalizer = ErrorTotalizer(directory_csv_output)

    def execute(self) -> None:
        """This method executes all CSV converters."""
        for path_csv_file in sorted(self.directory_csv_input.glob("*.csv")):
            self.error_totalizer.convert_csv(path_csv_file)
        if self.error_totalizer.is_presented:
            self.error_totalizer.export_to_csv()
            raise SomeInvalidInputCsvError(self.error_totalizer.message)
