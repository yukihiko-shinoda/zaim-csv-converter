"""This module implements error report process for input CSV."""

from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import Generic
from typing import Union

from zaimcsvconverter.inputtooutput.datasources import DataSource
from zaimcsvconverter.inputtooutput.datasources.csvfile.csv_file import Csv
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import TypeVarInputRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import TypeVarInputRow


class DataSourceErrorReporter(ABC):
    @abstractmethod
    def __iter__(self) -> Generator[list[Union[int, str]], None, None]:
        raise NotImplementedError


class InputCsvErrorReporter(Generic[TypeVarInputRow, TypeVarInputRowData], DataSourceErrorReporter):
    """This class implements error report process for input CSV."""

    def __init__(self, csv: Csv[TypeVarInputRow, TypeVarInputRowData]) -> None:
        self.csv = csv

    def __iter__(self) -> Generator[list[Union[int, str]], None, None]:
        if self.csv.invalid_header_error is not None:
            yield [self.csv.first_form_normalizer.path_to_file.name, "", str(self.csv.invalid_header_error)]
        if self.csv.invalid_footer_error is not None:
            yield [self.csv.first_form_normalizer.path_to_file.name, "", str(self.csv.invalid_footer_error)]
        for index, list_error in self.csv.dictionary_invalid_record.items():
            for error in list_error:
                yield [self.csv.first_form_normalizer.path_to_file.name, index, str(error)]


class DataSourceErrorReporterFactory:
    """Creates DataSourceErrorReporter instance."""

    @staticmethod
    def create(data_source: DataSource) -> DataSourceErrorReporter:
        if isinstance(data_source, Csv):
            return InputCsvErrorReporter(data_source)
        raise TypeError
