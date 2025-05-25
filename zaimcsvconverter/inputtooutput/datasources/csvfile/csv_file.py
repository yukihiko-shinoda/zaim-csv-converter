"""CSV datasource."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Generic
from typing import Optional
from typing import cast

from godslayer.exceptions import InvalidFooterError
from godslayer.exceptions import InvalidHeaderError
from pydantic import ValidationError

from zaimcsvconverter.exceptions import InvalidCellError
from zaimcsvconverter.exceptions import InvalidRecordError
from zaimcsvconverter.exceptions import LogicError
from zaimcsvconverter.exceptions import SkipRecord
from zaimcsvconverter.exceptions.invalid_input_csv_error import InvalidInputCsvError
from zaimcsvconverter.inputtooutput.datasources import AbstractInputRecord
from zaimcsvconverter.inputtooutput.datasources import DataSource
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import TypeVarInputRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import TypeVarInputRow

if TYPE_CHECKING:
    from collections.abc import Generator

    from zaimcsvconverter.first_form_normalizer import FirstFormNormalizer
    from zaimcsvconverter.inputtooutput.datasources.csvfile.csv_record_processor import CsvRecordProcessor


class Csv(Generic[TypeVarInputRow, TypeVarInputRowData], DataSource):
    """This class implements CSV datasource."""

    def __init__(
        self,
        first_form_normalizer: FirstFormNormalizer[TypeVarInputRowData],
        csv_record_processor: CsvRecordProcessor[TypeVarInputRowData, TypeVarInputRow],
    ) -> None:
        super().__init__()
        self.first_form_normalizer = first_form_normalizer
        self.csv_record_processor = csv_record_processor
        self.invalid_header_error: Optional[InvalidHeaderError] = None
        self.invalid_footer_error: Optional[InvalidFooterError] = None

    def __iter__(self) -> Generator[AbstractInputRecord, None, None]:
        iterator = self.first_form_normalizer.__iter__()
        while True:
            try:
                input_record_data = self.try_to_iterate(iterator)
            except ValidationError as exc:
                exception = self.build_invalid_record_error(exc)
                self.mark_current_record_as_error(exception.list_error)
                self.undefined_content_error_handler.extend(exception.undefined_content_error_handler)
                continue
            except StopIteration:
                break
            yield from self.convert_to_record(input_record_data)

    def try_to_iterate(self, iterator: Generator[TypeVarInputRowData, None, None]) -> TypeVarInputRowData:
        """Try to iterate CSV row data."""
        try:
            return next(iterator)
        except InvalidHeaderError as error:
            self.invalid_header_error = error
            raise InvalidInputCsvError(self, str(error)) from error
        except InvalidFooterError as error:
            self.invalid_footer_error = error
            raise InvalidInputCsvError(self, str(error)) from error

    def convert_to_record(self, input_record_data: TypeVarInputRowData) -> Generator[AbstractInputRecord, None, None]:
        """Converts InputRecordData to InputRecord."""
        try:
            yield cast("AbstractInputRecord", self.csv_record_processor.execute(input_record_data))
        except InvalidRecordError as exc:
            self.mark_current_record_as_error(exc.list_error)
            self.undefined_content_error_handler.extend(exc.undefined_content_error_handler)
        except SkipRecord:
            pass

    def build_invalid_record_error(self, exc: ValidationError) -> InvalidRecordError:
        list_error = [InvalidCellError(f"Invalid {error['loc'][0]}, {error['msg']}") for error in exc.errors()]
        return InvalidRecordError(list_error)

    @property
    def is_invalid(self) -> bool:
        return (
            bool(self.dictionary_invalid_record)
            or self.invalid_header_error is not None
            or self.invalid_footer_error is not None
        )

    def mark_current_record_as_error(self, list_error: list[InvalidCellError]) -> None:
        if self.first_form_normalizer.index is None:  # pragma: no cover
            msg = "This method can't be called before iterate this instance."
            raise LogicError(msg)
        self.dictionary_invalid_record[self.first_form_normalizer.index] = list_error

    @property
    def message(self) -> str:
        return (
            "Undefined store or item name in convert table CSV exists "
            f"in {self.first_form_normalizer.path_to_file.name}. "
            "Please check property AccountCsvConverter.list_undefined_store."
        )
