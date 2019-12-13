"""This module implements model of input CSV."""
import csv
import re
from pathlib import Path
from typing import Dict, Optional, List

from zaimcsvconverter.account import Account
from zaimcsvconverter.error_collector import SingleErrorCollector
from zaimcsvconverter.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.exceptions import InvalidHeaderError, InvalidInputCsvError, InvalidRowError, SkipRow
from zaimcsvconverter.row_processor import RowProcessor


class InputCsv:
    """This class implements model of input CSV."""
    def __init__(self, path_to_file: Path):
        self.path_to_file: Path = path_to_file
        self._account = Account.create_by_path_csv_input(path_to_file)
        self.undefined_content_error_handler: UndefinedContentErrorHandler = UndefinedContentErrorHandler()
        self.invalid_header_error: Optional[InvalidHeaderError] = None
        self.dictionary_invalid_row: Dict[int, List[InvalidRowError]] = {}

    @property
    def is_invalid(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.invalid_header_error is not None or bool(self.dictionary_invalid_row)

    def covert_to_zaim(self, writer_zaim) -> None:
        """This method convert this csv into Zaim format CSV."""
        account_context = self._account.value
        with self.path_to_file.open('r', encoding=account_context.encode) as file_input:
            reader_input = csv.reader(file_input)
            if account_context.csv_header:
                self._skip_header(reader_input)
            for index, list_input_row_standard_type_value in enumerate(reader_input):
                self._process_row(index, list_input_row_standard_type_value, writer_zaim)
        if self.is_invalid:
            raise InvalidInputCsvError(
                f'Undefined store name in convert table CSV exists in {self.path_to_file.name}. '
                'Please check property AccountCsvConverter.list_undefined_store.'
            )

    def _skip_header(self, reader_input):
        error_message = (f'{self.path_to_file.name} does not include header row.'
                         'Please confirm AccountConfig.csv_header. '
                         f'AccountConfig.csv_header = {self._account.value.csv_header}')
        error_collector = SingleErrorCollector(InvalidHeaderError, error_message)
        with error_collector:
            while True:
                row = reader_input.__next__()
                if len(row) != len(self._account.value.csv_header):
                    continue
                is_header = True
                for column, header_column in zip(row, self._account.value.csv_header):
                    pattern = re.compile(header_column, re.UNICODE)
                    if column != header_column and not pattern.search(column):
                        is_header = False
                        break
                if is_header:
                    break
        if error_collector.error is not None:
            self.invalid_header_error = error_collector.error
            raise InvalidInputCsvError(error_message) from error_collector.error

    def _process_row(self, index: int, list_input_row_standard_type_value: List[str], writer_zaim) -> None:
        row_processor = RowProcessor(self._account)
        try:
            zaim_row = row_processor.execute(list_input_row_standard_type_value)
        except InvalidRowError:
            self._stock_error(index, row_processor)
            return
        except SkipRow:
            return
        writer_zaim.writerow(zaim_row.convert_to_list())

    def _stock_error(self, index: int, row_processor: RowProcessor):
        self.dictionary_invalid_row[index] = row_processor.list_error
        self.undefined_content_error_handler.extend(row_processor.undefined_content_error_handler)
