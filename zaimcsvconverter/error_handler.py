"""This module implements error handler."""
from __future__ import annotations
from typing import List

import numpy

from zaimcsvconverter.account import Account
from zaimcsvconverter.input_row import InputRowData


class ErrorHandler:
    """This class implements error handler."""
    def __init__(self):
        self.list_error: List[List[str]] = []

    def __iter__(self):
        for error_row in self.list_error:
            yield error_row

    def append_undefined_content(self, account: Account, input_row_data: InputRowData) -> None:
        """This method appends error list argument into error list property."""
        self.list_error.append([
            account.value.file_name_csv_convert,
            input_row_data.store_name,
            input_row_data.item_name
        ])

    def extend(self, error_handler: ErrorHandler) -> None:
        """This method extends error list argument into error list property."""
        self.list_error.extend(error_handler.list_error)

    @property
    def is_presented(self) -> bool:
        """This property returns whether error is presented or not."""
        return bool(self.list_error)

    def uniquify(self) -> None:
        """This method uniquify error list."""
        self.list_error = numpy.unique(self.list_error, axis=0).tolist()
