"""This module implements checker for output CSV file."""
import csv
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Type, List, Generic, TypeVar

from fixturefilehandler.file_paths import RelativeDeployFilePath

from tests.testlibraries.row_data import InvalidRowErrorRowData, ZaimRowData
from zaimcsvconverter.zaim_row import ZaimRow

TypeVarOutputRowData = TypeVar('TypeVarOutputRowData')


# @see https://github.com/python/mypy/issues/5374
@dataclass
class OutputCsvFileChecker(Generic[TypeVarOutputRowData]):  # type: ignore
    """This class helps to check output CSV file."""
    directory_csv_output: RelativeDeployFilePath
    output_row_data_class: Type[TypeVarOutputRowData] = field(init=False)

    def assert_file(self, file_name: str, list_expected: List[TypeVarOutputRowData]):
        """This method checks Zaim CSV file."""
        list_output_row_data: List[TypeVarOutputRowData] = self.read_output_csv(file_name)
        assert len(list_output_row_data) == len(list_expected), (
            f'len(list_output_row_data) = {len(list_output_row_data)}, len(list_expected) = {len(list_expected)}'
        )
        for output_row_data, expected in zip(list_output_row_data, list_expected):
            assert output_row_data == expected, f'output_row_data = {output_row_data}'

    def read_output_csv(self, file_name: str) -> List[TypeVarOutputRowData]:
        """This method reads output CSV files and returns as list of output row data instance."""
        list_zaim_row_data = []
        with (self.directory_csv_output.target / file_name).open('r', encoding='UTF-8', newline='\n') as file:
            csv_reader = csv.reader(file)
            self.assert_header_and_skip(csv_reader)
            for list_row_data in csv_reader:
                # Reason: Pylint has not support dataclasses. pylint: disable=not-callable
                list_zaim_row_data.append(self.output_row_data_class(*list_row_data))  # type: ignore
        return list_zaim_row_data

    @abstractmethod
    def assert_header_and_skip(self, csv_reader) -> None:
        """This method reads output CSV files and returns as list of output row data instance."""


@dataclass
class ZaimCsvFileChecker(OutputCsvFileChecker):
    """This class helps to check Zaim CSV file."""
    output_row_data_class: Type[ZaimRowData] = field(default=ZaimRowData, init=False)

    def assert_header_and_skip(self, csv_reader) -> None:
        assert csv_reader.__next__() == ZaimRow.HEADER


@dataclass
class ErrorCsvFileChecker(OutputCsvFileChecker):
    """This class helps to check Zaim CSV file."""
    output_row_data_class: Type[InvalidRowErrorRowData] = field(default=InvalidRowErrorRowData, init=False)

    def assert_header_and_skip(self, csv_reader) -> None:
        pass
