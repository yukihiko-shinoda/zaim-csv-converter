"""This module implements totalize process of error."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from zaimcsvconverter.csvconverter.csv_to_csv_converter import CsvToCsvConverter
from zaimcsvconverter.errorhandling.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.errorreporters.csv_exporter import CsvExporter
from zaimcsvconverter.errorreporters.input_csv_error_reporter import DataSourceErrorReporterFactory
from zaimcsvconverter.exceptions.invalid_input_csv_error import InvalidInputCsvError

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

    from zaimcsvconverter.inputtooutput.datasources import DataSource


class FileNameForError(Enum):
    INVALID_ROW = "error_invalid_row.csv"
    UNDEFINED_CONTENT = "error_undefined_content.csv"


class ErrorTotalizer:
    """This class implements totalize process of error."""

    def __init__(self, directory_csv_output: Path) -> None:
        self.directory_csv_output = directory_csv_output
        self.list_invalid_data_source: list[DataSource] = []
        self.undefined_content_error_handler: UndefinedContentErrorHandler = UndefinedContentErrorHandler()

    def __iter__(self) -> Generator[list[int | str], None, None]:
        for data_source in self.list_invalid_data_source:
            data_source_error_reporter = DataSourceErrorReporterFactory.create(data_source)
            yield from data_source_error_reporter

    def convert_csv(self, path_csv_file: Path) -> None:
        """To seal complexity in for loop."""
        csv_to_csv_converter = CsvToCsvConverter(path_csv_file, self.directory_csv_output)
        try:
            csv_to_csv_converter.execute()
        except InvalidInputCsvError as exc:
            self.list_invalid_data_source.append(exc.data_source)
            self.undefined_content_error_handler.extend(exc.data_source.undefined_content_error_handler)

    @property
    def is_presented(self) -> bool:
        return bool(self.list_invalid_data_source)

    def report_to_csv(self) -> None:
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
                self.undefined_content_error_handler,  # type: ignore[arg-type]
                FileNameForError.UNDEFINED_CONTENT.value,
            )

    @property
    def message(self) -> str:
        """This property returns error message."""
        message = f"Some invalid input CSV file exists. Please check {FileNameForError.INVALID_ROW.value}"
        if self.undefined_content_error_handler.is_presented:
            message = message + f" and {FileNameForError.UNDEFINED_CONTENT.value}"
        return f"{message}."
