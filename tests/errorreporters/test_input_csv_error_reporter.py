"""Tests for zaimcsvconverter.errorreporters.input_csv_error_reporter."""
from typing import Generator, Generic, List

import pytest

from zaimcsvconverter.errorreporters.input_csv_error_reporter import DataSourceErrorReporterFactory
from zaimcsvconverter.exceptions import InvalidCellError
from zaimcsvconverter.inputtooutput.datasources import AbstractInputRecord, DataSource
from zaimcsvconverter.inputtooutput.datasources.csv.data import TypeVarInputRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import TypeVarInputRow


class TestInputCsvErrorReporter:
    """Tests for InputCsvErrorReporter."""

    @staticmethod
    def test_error() -> None:
        """Method create() should raise appropriate error."""

        class Unexpected(Generic[TypeVarInputRow, TypeVarInputRowData], DataSource):
            """Unexpected class."""

            def __iter__(self) -> Generator[AbstractInputRecord, None, None]:
                pass

            def mark_current_record_as_error(self, list_error: List[InvalidCellError]) -> None:
                pass

            @property
            def is_invalid(self) -> bool:
                return False

            @property
            def message(self) -> str:
                return ""

        with pytest.raises(TypeError):
            DataSourceErrorReporterFactory.create(Unexpected())
