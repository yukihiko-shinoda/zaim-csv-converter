"""This module implements error handler."""
from __future__ import annotations

from enum import Enum
from typing import List

import numpy

from zaimcsvconverter.account import FileNameCsvConvert
from zaimcsvconverter.inputcsvformats import InputRowData


class FileNameError(Enum):
    # Reason: Raw code is simple enough. pylint: disable=missing-docstring
    INVALID_ROW: str = 'error_invalid_row.csv'
    UNDEFINED_CONTENT: str = 'error_undefined_content.csv'


class UndefinedContentErrorHandler:
    """This class implements undefined content error handler."""

    def __init__(self):
        self.list_error: List[List[str]] = []

    def __iter__(self):
        for error_row in self.list_error:
            yield error_row

    def append(self, file_name_csv_convert: FileNameCsvConvert, input_row_data: InputRowData) -> None:
        """This method appends error list argument into error list property."""
        self.list_error.append([
            file_name_csv_convert.value,
            input_row_data.store_name,
            input_row_data.item_name
        ])

    def extend(self, error_handler: UndefinedContentErrorHandler) -> None:
        """This method extends error list argument into error list property."""
        if not error_handler.is_presented:
            return
        error_handler.uniquify()
        self.list_error.extend(error_handler.list_error)
        self.uniquify()

    @property
    def is_presented(self) -> bool:
        """This property returns whether error is presented or not."""
        return bool(self.list_error)

    def uniquify(self) -> None:
        """This method uniquify error list."""
        self.list_error = numpy.unique(self.list_error, axis=0).tolist()
