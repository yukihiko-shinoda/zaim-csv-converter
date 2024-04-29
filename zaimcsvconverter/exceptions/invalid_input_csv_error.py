"""To prevent circular import."""

from zaimcsvconverter.exceptions import Error
from zaimcsvconverter.inputtooutput.datasources import DataSource


class InvalidInputCsvError(Error):
    """Target input CSV is invalid.

    This error is only for processing control and display to standard error. Not for write error CSV.
    """

    def __init__(
        self,
        data_source: DataSource,
        *args: object,
    ) -> None:
        self.data_source = data_source
        super().__init__(*args)
