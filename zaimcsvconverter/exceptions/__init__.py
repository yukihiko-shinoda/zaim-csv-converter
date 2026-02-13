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
        message: str,
        list_error: list[InvalidCellError],
        undefined_content_error_handler: UndefinedContentErrorHandler,
    ) -> None:
        super().__init__(message, list_error, undefined_content_error_handler)
        self.message = message
        self.list_error = list_error
        self.undefined_content_error_handler = undefined_content_error_handler

    def __str__(self) -> str:
        """Return formatted error message."""
        return self.message


class InvalidRecordErrorFactory:
    """Factory class for creating InvalidRecordError instances."""

    @staticmethod
    def create(
        list_error: list[InvalidCellError],
        *,
        undefined_content_error_handler: UndefinedContentErrorHandler | None = None,
    ) -> InvalidRecordError:
        """Create an InvalidRecordError with a formatted message.

        Args:
            list_error: List of cell errors
            undefined_content_error_handler: Handler for undefined content errors

        Returns:
            InvalidRecordError instance with formatted message
        """
        error_messages = ", ".join(str(error) for error in list_error)
        message = f"Invalid record: {error_messages}"
        handler = undefined_content_error_handler
        return InvalidRecordError(message, list_error, handler or UndefinedContentErrorHandler())


class SomeInvalidInputCsvError(Error):
    pass
