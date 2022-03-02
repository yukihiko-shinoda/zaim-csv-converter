"""This module implements totalize process of error."""
from pathlib import Path
from typing import Generator, List, Union

from zaimcsvconverter.csvconverter.input_csv_converter import InputCsvConverter
from zaimcsvconverter.csvconverter.input_data import InputData
from zaimcsvconverter.errorhandling.error_handler import FileNameForError, UndefinedContentErrorHandler
from zaimcsvconverter.errorreporters.csv_exporter import CsvExporter
from zaimcsvconverter.errorreporters.input_csv_error_reporter import DataSourceErrorReporterFactory
from zaimcsvconverter.exceptions import InvalidInputCsvError


class ErrorTotalizer:
    """This class implements totalize process of error."""

    def __init__(self, directory_csv_output: Path) -> None:
        self.directory_csv_output = directory_csv_output
        self.list_invalid_input_data: List[InputData] = []
        self.undefined_content_error_handler: UndefinedContentErrorHandler = UndefinedContentErrorHandler()

    def __iter__(self) -> Generator[List[Union[int, str]], None, None]:
        for input_data in self.list_invalid_input_data:
            data_source_error_reporter = DataSourceErrorReporterFactory.create(input_data.data_source)
            yield from data_source_error_reporter

    def convert_csv(self, path_csv_file: Path) -> None:
        csv_converter = InputCsvConverter(path_csv_file, self.directory_csv_output)
        try:
            csv_converter.execute()
        except InvalidInputCsvError:
            input_data = csv_converter.input_csv
            self.list_invalid_input_data.append(input_data)
            self.undefined_content_error_handler.extend(input_data.undefined_content_error_handler)

    @property
    def is_presented(self) -> bool:
        return bool(self.list_invalid_input_data)

    def export_to_csv(self) -> None:
        """This method exports invalid input CSV errors into CSV."""
        csv_exporter = CsvExporter(self.directory_csv_output)
        csv_exporter.export(self, FileNameForError.INVALID_ROW.value)
        if self.undefined_content_error_handler.is_presented:
            csv_exporter.export(
                # Reason: mypy's bug. Iterator[List[str]] should be included in Iterator[List[Union[str, int]]] .
                # error: Argument 1 to "export" of "CsvExporter" has incompatible type "UndefinedContentErrorHandler";
                #        expected "Iterable[List[Union[str, int]]]"
                # note: Following member(s) of "UndefinedContentErrorHandler" have conflicts:
                # note:     Expected:
                # note:         def __iter__(self) -> Iterator[List[Union[str, int]]]
                # note:     Got:
                # note:         def __iter__(self) -> Iterator[List[str]]
                self.undefined_content_error_handler,  # type: ignore
                FileNameForError.UNDEFINED_CONTENT.value,
            )

    @property
    def message(self) -> str:
        """This property returns error message."""
        message = "Some invalid input CSV file exists. " f"Please check {FileNameForError.INVALID_ROW.value}"
        if self.undefined_content_error_handler.is_presented:
            message = message + f" and {FileNameForError.UNDEFINED_CONTENT.value}"
        return f"{message}."
