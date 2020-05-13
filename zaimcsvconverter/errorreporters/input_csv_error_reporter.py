"""This module implements error report process for input CSV."""
from typing import Generator, List, Union

from zaimcsvconverter.datasources.csv import Csv
from zaimcsvconverter.datasources.data_source import DataSource


class InputCsvErrorReporter:
    """This class implements error report process for input CSV."""
    def __init__(self, csv: Csv):
        self.csv = csv

    def __iter__(self) -> Generator[List[Union[int, str]], None, None]:
        if self.csv.invalid_header_error is not None:
            yield [self.csv.god_slayer.path_to_file.name, '', str(self.csv.invalid_header_error)]
        if self.csv.invalid_footer_error is not None:
            yield [self.csv.god_slayer.path_to_file.name, '', str(self.csv.invalid_footer_error)]
        for index, list_error in self.csv.dictionary_invalid_record.items():
            for error in list_error:
                yield [self.csv.god_slayer.path_to_file.name, index, str(error)]


class DataSourceErrorReporterFactory:
    """This class creates ImputCsvErrorReporter instance."""
    @staticmethod
    def create(data_source: DataSource):
        """Creates InputCsvErrorReporter instance."""
        if isinstance(data_source, Csv):
            return InputCsvErrorReporter(data_source)
        raise TypeError()
