"""This module implements exceptions for this package."""
from godslayer.exceptions import InvalidRecordError


class Error(Exception):
    """
    Base class for exceptions in this module.
    @see https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
    """


class LogicError(Error):
    """This Error indicates programing miss."""


class SkipRow(Error):
    """Target row is invalid."""


class UndefinedContentError(InvalidRecordError):
    """Store or item is undefined."""


class InvalidInputCsvError(Error):
    """
    Target input CSV is invalid.
    This error is only for processing control and display to standard error.
    Not for write error CSV.
    """
