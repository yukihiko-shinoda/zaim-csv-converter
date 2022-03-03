"""Tests for zaimcsvconverter.errorreporters.input_csv_error_reporter."""
from typing import Generator, List

import pytest
from returns.primitives.hkt import Kind1

from zaimcsvconverter.datasources.data_source import DataSource
from zaimcsvconverter.errorreporters.input_csv_error_reporter import DataSourceErrorReporterFactory
from zaimcsvconverter.exceptions import InvalidCellError
from zaimcsvconverter.inputcsvformats import TypeVarInputRow, TypeVarInputRowData


class TestInputCsvErrorReporter:
    """Tests for InputCsvErrorReporter."""

    @staticmethod
    def test_error() -> None:
        """Method create() should raise appropriate error."""

        class Unexpected(DataSource[TypeVarInputRow, TypeVarInputRowData]):
            """Unexpected class."""

            def __iter__(self) -> Generator[Kind1[TypeVarInputRow, TypeVarInputRowData], None, None]:
                pass

            def mark_current_record_as_error(self, list_error: List[InvalidCellError]) -> None:
                pass

            @property
            def is_invalid(self) -> bool:
                return False

            def raise_error_if_invalid(self) -> None:
                pass

        with pytest.raises(TypeError):
            DataSourceErrorReporterFactory.create(Unexpected())
