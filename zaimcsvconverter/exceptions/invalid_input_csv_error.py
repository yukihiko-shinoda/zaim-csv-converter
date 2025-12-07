"""To prevent circular import."""

from zaimcsvconverter.exceptions import Error
from zaimcsvconverter.inputtooutput.datasources import DataSource


class InvalidInputCsvError(Error):
    """Target input CSV is invalid.

    This error is only for processing control and display to standard error. Not for write error CSV.
    """

    def __init__(
        self,
        message: str,
        data_source: DataSource,
    ) -> None:
        super().__init__(message, data_source)
        self.message = message
        self.data_source = data_source

    def __str__(self) -> str:
        """Return just the message for string representation."""
        return self.message
