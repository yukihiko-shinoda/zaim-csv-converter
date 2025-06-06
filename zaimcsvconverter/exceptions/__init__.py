"""This module implements exceptions for this package."""

from __future__ import annotations

from zaimcsvconverter.errorhandling.error_handler import UndefinedContentErrorHandler


class Error(Exception):
    """Base class for exceptions in this module.

    @see https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
    """


class LogicError(Error):
    """This Error indicates programing miss."""


# Reason: Intentionally named.
class SkipRecord(Error):  # noqa: N818
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
        *args: object,
        undefined_content_error_handler: UndefinedContentErrorHandler | None = None,
    ) -> None:
        self.list_error = list_error
        self.undefined_content_error_handler = (
            UndefinedContentErrorHandler()
            if undefined_content_error_handler is None
            else undefined_content_error_handler
        )
        super().__init__(*args)


class SomeInvalidInputCsvError(Error):
    pass
