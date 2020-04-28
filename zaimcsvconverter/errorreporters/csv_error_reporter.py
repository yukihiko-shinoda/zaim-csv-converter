"""This module implements error report process for CSV reader."""
from typing import Generator, List, Union, Generic

from zaimcsvconverter.datasources.csv import AbstractCsv, Csv, TypeVarCsv
from zaimcsvconverter.datasources.csv_with_header import CsvWithHeader, TypeVarCsvWithHeader
from zaimcsvconverter.datasources.view_card_csv import ViewCardCsv


class CsvErrorReporter(Generic[TypeVarCsv]):
    def __init__(self, csv: TypeVarCsv):
        self.csv = csv

    def __iter__(self) -> Generator[List[Union[int, str]], None, None]:
        raise NotImplementedError()  # pragma: no cover


class CsvWithHeaderErrorReporter(CsvErrorReporter[TypeVarCsvWithHeader]):
    def __iter__(self) -> Generator[List[Union[int, str]], None, None]:
        if self.csv.invalid_header_error is not None:
            yield [self.csv.csv_reader.path_to_file.name, '', str(self.csv.invalid_header_error)]


class CsvErrorReporterFactory:
    @staticmethod
    def create(csv: AbstractCsv):
        if isinstance(csv, (ViewCardCsv, CsvWithHeader)):
            return CsvWithHeaderErrorReporter(csv)
        if isinstance(csv, Csv):
            return CsvErrorReporter(csv)
        else:
            raise TypeError()
