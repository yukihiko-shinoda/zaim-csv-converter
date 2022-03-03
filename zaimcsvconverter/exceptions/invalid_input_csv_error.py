"""To prevent circular import."""
from typing import Generic

from zaimcsvconverter.datasources.data_source import DataSource
from zaimcsvconverter.exceptions import Error
from zaimcsvconverter.inputcsvformats import TypeVarInputRow, TypeVarInputRowData


class InvalidInputCsvError(Generic[TypeVarInputRow, TypeVarInputRowData], Error):
    """Target input CSV is invalid.

    This error is only for processing control and display to standard error. Not for write error CSV.
    """

    def __init__(
        self,
        data_source: DataSource[TypeVarInputRow, TypeVarInputRowData],
        *args: object,
    ) -> None:
        self.data_source = data_source
        super().__init__(*args)
