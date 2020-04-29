"""This module implements exceptions for this package."""


class Error(Exception):
    """
    Base class for exceptions in this module.
    @see https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
    """


class InvalidRecordError(Error):
    """Target record is invalid."""


class InvalidHeaderError(InvalidRecordError):
    """Header record is invalid."""
