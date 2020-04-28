"""This module implements error report process for input CSV."""
from typing import Generator, List, Union

from zaimcsvconverter.datasources.csv import AbstractCsv
from zaimcsvconverter.datasources.data_source import DataSource
from zaimcsvconverter.errorreporters.csv_error_reporter import CsvErrorReporterFactory


class InputCsvErrorReporter:
    def __init__(self, csv: AbstractCsv):
        self.csv = csv

    def __iter__(self) -> Generator[List[Union[int, str]], None, None]:
        csv_reader_error_reporter = CsvErrorReporterFactory.create(self.csv)
        yield from csv_reader_error_reporter
        for index, list_error in self.csv.dictionary_invalid_record.items():
            for error in list_error:
                yield [self.csv.csv_reader.path_to_file.name, index, str(error)]


class DataSourceErrorReporterFactory:
    @staticmethod
    def create(data_source: DataSource):
        if isinstance(data_source, AbstractCsv):
            return InputCsvErrorReporter(data_source)
        else:
            raise TypeError()
