"""This module implements CSV with header model."""
from pathlib import Path
from typing import List, Optional, Generator, Any, Generic, TypeVar

from godslayer.csv_with_header_reader import CsvWithHeaderReader, TypeVarCsvWithHeaderReader
from godslayer.exceptions import InvalidHeaderError
from zaimcsvconverter.datasources.csv import AbstractCsv, CsvFactory
from zaimcsvconverter.exceptions import InvalidInputCsvError


class AbstractCsvWithHeader(AbstractCsv, Generic[TypeVarCsvWithHeaderReader]):
    """This class implements analyzing process of CSV with header."""
    def __init__(self, csv_with_header_reader: TypeVarCsvWithHeaderReader):
        super().__init__(csv_with_header_reader)
        self.invalid_header_error: Optional[InvalidHeaderError] = None

    def __iter__(self) -> Generator[List[Any], None, None]:
        try:
            yield from self.csv_reader
        except InvalidHeaderError as error:
            self.invalid_header_error = error
            raise InvalidInputCsvError(str(error)) from error

    @property
    def is_invalid(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return super().is_invalid or self.invalid_header_error is not None


class CsvWithHeader(AbstractCsvWithHeader):
    """This class implements analyzing process of CSV with header."""
    def __init__(self, path_to_file: Path, header: List[str], encode: str = 'UTF-8'):
        super().__init__(CsvWithHeaderReader(path_to_file, header, encode))


TypeVarCsvWithHeader = TypeVar('TypeVarCsvWithHeader', bound=CsvWithHeader)


class CsvWithHeaderFactory(CsvFactory):
    """This class implements factory method for CsvWithHeaderReader."""
    def __init__(self, header: List[str], encode: str = 'UTF-8'):
        super().__init__(encode)
        self.header = header

    def create(self, path_to_file: Path):
        return CsvWithHeader(path_to_file, self.header, self.encode)
