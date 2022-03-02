"""This module implements exceptions for this package."""


from typing import Optional

from zaimcsvconverter.errorhandling.error_handler import UndefinedContentErrorHandler


class Error(Exception):
    """Base class for exceptions in this module.

    @see https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
    """


class LogicError(Error):
    """This Error indicates programing miss."""


class SkipRecord(Error):
    """Target row is invalid."""


class InvalidCellError(Error):
    """Cell is invalid."""


class UndefinedContentError(InvalidCellError):
    """Store or item is undefined."""


class InvalidRecordError(Error):
    """Record is invalid."""

    def __init__(
        self,
        list_error: list[InvalidCellError],
        undefined_content_error_handler: Optional[UndefinedContentErrorHandler] = None,
        *args: object
    ) -> None:
        self.list_error = list_error
        self.undefined_content_error_handler = (
            UndefinedContentErrorHandler()
            if undefined_content_error_handler is None
            else undefined_content_error_handler
        )
        super().__init__(*args)


class InvalidInputCsvError(Error):
    """Target input CSV is invalid.

    This error is only for processing control and display to standard error. Not for write error CSV.
    """
