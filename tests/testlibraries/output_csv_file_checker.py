"""This module implements checker for output CSV file."""

import csv
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import Generic
from typing import TypeVar

from fixturefilehandler.file_paths import RelativeDeployFilePath

from tests.testlibraries.row_data import InvalidRowErrorRowData
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.inputtooutput.exporters.zaim.csvfile.csv_types import CSVReader
from zaimcsvconverter.inputtooutput.exporters.zaim.csvfile.zaim_csv_format import ZaimCsvFormat

TypeVarOutputRowData = TypeVar("TypeVarOutputRowData")


@dataclass
class OutputCsvFileChecker(Generic[TypeVarOutputRowData]):
    """This class helps to check output CSV file."""

    directory_csv_output: RelativeDeployFilePath
    output_row_data_class: type[TypeVarOutputRowData] = field(init=False)

    def assert_file(self, file_name: str, list_expected: list[TypeVarOutputRowData]) -> None:
        """This method checks Zaim CSV file."""
        list_output_row_data: list[TypeVarOutputRowData] = self.read_output_csv(file_name)
        assert len(list_output_row_data) == len(
            list_expected,
        ), f"len(list_output_row_data) = {len(list_output_row_data)}, len(list_expected) = {len(list_expected)}"
        for output_row_data, expected in zip(list_output_row_data, list_expected):
            assert output_row_data == expected, self._build_error_message(
                expected,
                list_output_row_data,
                output_row_data,
            )

    @staticmethod
    def _build_error_message(
        expected: TypeVarOutputRowData,
        list_output_row_data: list[TypeVarOutputRowData],
        output_row_data: TypeVarOutputRowData,
    ) -> str:
        debug_list_output_row_data = ",\n".join(str(output_row_data) for output_row_data in list_output_row_data)
        return f"\n{expected=}\n{output_row_data=}\nlist_output_row_data={debug_list_output_row_data}"

    def read_output_csv(self, file_name: str) -> list[TypeVarOutputRowData]:
        """This method reads output CSV files and returns as list of output row data instance."""
        with (self.directory_csv_output.target / file_name).open("r", encoding="UTF-8", newline="\n") as file:
            csv_reader = csv.reader(file)
            self.assert_header_and_skip(csv_reader)
            return [
                # Reason: Pylint has not support dataclasses. pylint: disable=not-callable
                self.output_row_data_class(*list_row_data)
                for list_row_data in csv_reader
            ]

    @abstractmethod
    def assert_header_and_skip(self, csv_reader: CSVReader) -> None:
        """This method reads output CSV files and returns as list of output row data instance."""


@dataclass
class ZaimCsvFileChecker(OutputCsvFileChecker[ZaimRowData]):
    """This class helps to check Zaim CSV file."""

    output_row_data_class: type[ZaimRowData] = field(default=ZaimRowData, init=False)

    def assert_header_and_skip(self, csv_reader: CSVReader) -> None:
        assert next(csv_reader) == ZaimCsvFormat.HEADER


@dataclass
class ErrorCsvFileChecker(OutputCsvFileChecker[InvalidRowErrorRowData]):
    """This class helps to check Zaim CSV file."""

    output_row_data_class: type[InvalidRowErrorRowData] = field(default=InvalidRowErrorRowData, init=False)

    def assert_header_and_skip(self, csv_reader: CSVReader) -> None:
        pass
