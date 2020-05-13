from typing import List, Generator, Any

import pytest
from godslayer.exceptions import InvalidRecordError

from zaimcsvconverter.datasources.data_source import DataSource
from zaimcsvconverter.errorreporters.input_csv_error_reporter import DataSourceErrorReporterFactory


class TestInputCsvErrorReporter:
    @staticmethod
    def test_error():
        class Unexpected(DataSource):
            def __iter__(self) -> Generator[List[Any], None, None]:
                pass

            def mark_current_record_as_error(self, list_error: List[InvalidRecordError]):
                pass

            @property
            def is_invalid(self) -> bool:
                return False

            def raise_error_if_invalid(self) -> None:
                pass

        with pytest.raises(TypeError):
            DataSourceErrorReporterFactory.create(Unexpected())
