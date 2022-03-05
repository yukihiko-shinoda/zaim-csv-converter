"""This module implements CSV Datasource."""
from typing import cast, Generator, Generic, List, Optional

from godslayer.csv.god_slayer import GodSlayer
from godslayer.exceptions import InvalidFooterError, InvalidHeaderError

from zaimcsvconverter.csvconverter.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.datasources.data_source import AbstractInputRecord, DataSource
from zaimcsvconverter.exceptions.invalid_input_csv_error import InvalidInputCsvError
from zaimcsvconverter.exceptions import InvalidCellError, InvalidRecordError, LogicError, SkipRecord
from zaimcsvconverter.inputcsvformats import TypeVarInputRow, TypeVarInputRowData


class Csv(Generic[TypeVarInputRow, TypeVarInputRowData], DataSource):
    """This class implements abstract CSV Datasource."""

    def __init__(
        self, god_slayer: GodSlayer, csv_record_processor: CsvRecordProcessor[TypeVarInputRowData, TypeVarInputRow]
    ) -> None:
        super().__init__()
        self.god_slayer = god_slayer
        self.csv_record_processor = csv_record_processor
        self.invalid_header_error: Optional[InvalidHeaderError] = None
        self.invalid_footer_error: Optional[InvalidFooterError] = None

    def __iter__(self) -> Generator[AbstractInputRecord, None, None]:
        iterator = self.god_slayer.__iter__()
        while True:
            try:
                list_input_row_standard_type_value = next(iterator)
            except InvalidHeaderError as error:
                self.invalid_header_error = error
                raise InvalidInputCsvError(self, str(error)) from error
            except InvalidFooterError as error:
                self.invalid_footer_error = error
                raise InvalidInputCsvError(self, str(error)) from error
            except StopIteration:
                break
            try:
                yield cast(AbstractInputRecord, self.csv_record_processor.execute(list_input_row_standard_type_value))
            except InvalidRecordError as exc:
                self.mark_current_record_as_error(exc.list_error)
                self.undefined_content_error_handler.extend(exc.undefined_content_error_handler)
            except SkipRecord:
                pass

    @property
    def is_invalid(self) -> bool:
        return (
            bool(self.dictionary_invalid_record)
            or self.invalid_header_error is not None
            or self.invalid_footer_error is not None
        )

    def mark_current_record_as_error(self, list_error: List[InvalidCellError]) -> None:
        if self.god_slayer.index is None:
            raise LogicError("This method can't be called before iterate this instance.")  # pragma: no cover
        self.dictionary_invalid_record[self.god_slayer.index] = list_error

    def raise_error_if_invalid(self) -> None:
        if self.is_invalid:
            raise InvalidInputCsvError(
                self,
                f"Undefined store name in convert table CSV exists in {self.god_slayer.path_to_file.name}. "
                "Please check property AccountCsvConverter.list_undefined_store.",
            )
