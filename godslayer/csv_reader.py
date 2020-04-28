"""This module implements analyzing process of CSV."""
import csv
from pathlib import Path
from typing import Generator, List, Iterator, Optional, TypeVar


class CsvReader:
    """This class implements analyzing process of CSV."""
    def __init__(self, path_to_file: Path, encode: str = 'UTF-8'):
        self.path_to_file: Path = path_to_file
        self.encode = encode
        self.index: Optional[int] = None

    def __iter__(self) -> Generator[List[str], None, None]:
        # noinspection LongLine
        """
        This method convert this csv into Zaim format CSV.
        @see https://stackoverflow.com/questions/14797930/python-custom-iterator-close-a-file-on-stopiteration/14798115#14798115 # noqa
        """
        with self.path_to_file.open('r', encoding=self.encode) as file_input:
            reader_input: Iterator[List[str]] = csv.reader(file_input)
            yield from self._process_csv(reader_input)

    def _process_csv(self, reader_input: Iterator[List[str]]) -> Generator[List[str], None, None]:
        for self.index, list_input_row_standard_type_value in enumerate(reader_input):
            yield list_input_row_standard_type_value


TypeVarCsvReader = TypeVar('TypeVarCsvReader', bound=CsvReader)
