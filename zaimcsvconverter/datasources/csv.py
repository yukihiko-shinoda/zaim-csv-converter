"""This module implements CSV Datasource"""
from abc import ABC
from pathlib import Path
from typing import List, Generator, Any, TypeVar

from godslayer.csv_reader import TypeVarCsvReader, CsvReader
from godslayer.exceptions import InvalidRecordError
from zaimcsvconverter.datasources.data_source import DataSource
from zaimcsvconverter.exceptions import InvalidInputCsvError, LogicError


class AbstractCsv(DataSource, ABC):
    """This class implements abstract CSV Datasource"""
    def __init__(self, csv_reader: TypeVarCsvReader):
        super().__init__()
        self.csv_reader = csv_reader

    def __iter__(self) -> Generator[List[Any], None, None]:
        yield from self.csv_reader

    @property
    def is_invalid(self) -> bool:
        return bool(self.dictionary_invalid_record)

    def mark_current_record_as_error(self, list_error: List[InvalidRecordError]):
        if self.csv_reader.index is None:
            raise LogicError("This method can't be called before iterate this instance.")
        self.dictionary_invalid_record[self.csv_reader.index] = list_error

    def raise_error_if_invalid(self) -> None:
        if self.is_invalid:
            raise InvalidInputCsvError(
                f'Undefined store name in convert table CSV exists in {self.csv_reader.path_to_file.name}. '
                'Please check property AccountCsvConverter.list_undefined_store.'
            )


TypeVarCsv = TypeVar('TypeVarCsv', bound=AbstractCsv)


class Csv(AbstractCsv):
    """This class implements CSV Datasource"""
    def __init__(self, path_to_file: Path, encode: str = 'UTF-8'):
        super().__init__(CsvReader(path_to_file, encode))


class CsvFactory:
    """This class implements factory method for CsvReader."""
    def __init__(self, encode: str = 'UTF-8'):
        self.encode = encode

    def create(self, path_to_file: Path):
        """Creates CSV instance."""
        return Csv(path_to_file, self.encode)
