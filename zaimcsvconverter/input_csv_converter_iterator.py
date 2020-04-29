"""This module implements iterating steps from input_csv_converter."""
from pathlib import Path
from typing import Generator

from zaimcsvconverter.error_totalizer import ErrorTotalizer
from zaimcsvconverter.exceptions import InvalidInputCsvError
from zaimcsvconverter.input_csv_converter import InputCsvConverter


class InputCsvConverterIterator:
    """This class implements iterating steps from input_csv_converter."""

    def __init__(self, directory_csv_input: Path, directory_csv_output: Path):
        self.directory_csv_input = directory_csv_input
        self.directory_csv_output = directory_csv_output

    def execute(self) -> None:
        """This method executes all CSV converters."""
        error_aggregator = ErrorTotalizer()
        for csv_converter in self._list_csv_converter:
            try:
                csv_converter.execute()
            except InvalidInputCsvError:
                error_aggregator.append(csv_converter.input_csv)
        if error_aggregator.is_presented:
            error_aggregator.export_to_csv(self.directory_csv_output)
            raise InvalidInputCsvError(error_aggregator.message)

    @property
    def _list_csv_converter(self) -> Generator[InputCsvConverter, None, None]:
        return (InputCsvConverter(path_csv_file, self.directory_csv_output)
                for path_csv_file in self.directory_csv_input.glob('*.csv'))
