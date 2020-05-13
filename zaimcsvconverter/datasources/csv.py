"""This module implements CSV Datasource"""
from typing import List, Generator, Any, Optional

from godslayer.csv.god_slayer import GodSlayer
from godslayer.exceptions import InvalidRecordError, InvalidHeaderError, InvalidFooterError

from zaimcsvconverter.datasources.data_source import DataSource
from zaimcsvconverter.exceptions import InvalidInputCsvError, LogicError


class Csv(DataSource):
    """This class implements abstract CSV Datasource"""
    def __init__(self, god_slayer: GodSlayer):
        super().__init__()
        self.god_slayer = god_slayer
        self.invalid_header_error: Optional[InvalidHeaderError] = None
        self.invalid_footer_error: Optional[InvalidFooterError] = None

    def __iter__(self) -> Generator[List[Any], None, None]:
        try:
            yield from self.god_slayer
        except InvalidHeaderError as error:
            self.invalid_header_error = error
            raise InvalidInputCsvError(str(error)) from error
        except InvalidFooterError as error:
            self.invalid_footer_error = error
            raise InvalidInputCsvError(str(error)) from error

    @property
    def is_invalid(self) -> bool:
        return bool(
            self.dictionary_invalid_record
        ) or self.invalid_header_error is not None or self.invalid_footer_error is not None

    def mark_current_record_as_error(self, list_error: List[InvalidRecordError]):
        if self.god_slayer.index is None:
            raise LogicError("This method can't be called before iterate this instance.")  # pragma: no cover
        self.dictionary_invalid_record[self.god_slayer.index] = list_error

    def raise_error_if_invalid(self) -> None:
        if self.is_invalid:
            raise InvalidInputCsvError(
                f'Undefined store name in convert table CSV exists in {self.god_slayer.path_to_file.name}. '
                'Please check property AccountCsvConverter.list_undefined_store.'
            )
