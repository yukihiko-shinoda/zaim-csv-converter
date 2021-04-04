"""This module implements error handler."""
from __future__ import annotations

from enum import Enum
from typing import List

import numpy


class FileNameForError(Enum):
    INVALID_ROW: str = "error_invalid_row.csv"
    UNDEFINED_CONTENT: str = "error_undefined_content.csv"


class UndefinedContentErrorHandler:
    """This class implements undefined content error handler."""

    def __init__(self):
        self.list_error: List[List[str]] = []

    def __iter__(self):
        for error_row in self.list_error:
            yield error_row

    def extend_list(self, error: List[List[str]]) -> None:
        """This method appends error list argument into error list property."""
        self.list_error.extend(error)
        self.uniquify()

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
        # noinspection PyTypeChecker
        self.list_error = numpy.unique(numpy.array(self.list_error), axis=0).tolist()
