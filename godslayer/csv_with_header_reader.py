"""This module implements analyzing process of CSV with header."""
from pathlib import Path
from typing import Generator, List, Iterator, TypeVar

from godslayer.csv_reader import CsvReader
from errorcollector.error_collector import SingleErrorCollector
from godslayer.exceptions import InvalidHeaderError
from godslayer.row_pattern_matcher import RowPatternMatcher


class CsvWithHeaderReader(CsvReader):
    """This class implements analyzing process of CSV with header."""
    def __init__(self, path_to_file: Path, header: List[str], encode: str = 'UTF-8'):
        super().__init__(path_to_file, encode)
        self.header = header

    def _process_csv(self, reader_input: Iterator[List[str]]) -> Generator[List[str], None, None]:
        if self.header:
            self._skip_header(reader_input)
        yield from super()._process_csv(reader_input)

    def _skip_header(self, reader_input: Iterator[List[str]]):
        error_message = (f'{self.path_to_file.name} does not include header row.'
                         'Please confirm AccountConfig.header. '
                         f'AccountConfig.header = {self.header}')
        error_collector = SingleErrorCollector(InvalidHeaderError, error_message)
        with error_collector:
            self._try_skip_header(reader_input)
        if error_collector.error is not None:
            raise error_collector.error

    def _try_skip_header(self, reader_input: Iterator[List[str]]):
        while True:
            row = reader_input.__next__()
            if len(row) != len(self.header):
                continue
            if self._is_header(row):
                break

    def _is_header(self, row) -> bool:
        return RowPatternMatcher.is_matched(self.header, row)


TypeVarCsvWithHeaderReader = TypeVar('TypeVarCsvWithHeaderReader', bound=CsvWithHeaderReader)
