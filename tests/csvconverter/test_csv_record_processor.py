"""Tests for row_processror.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.account import Account
from zaimcsvconverter.csvconverter.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.exceptions import InvalidRecordError


class TestCsvRecordProcessor:
    """Tests for RecordProcessor."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema",
        [[InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO]],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test() -> None:
        """Tests following:

        - RecordProcessor should raise error when input row is invalid.
        - RecordProcessor should collect error when input row is invalid.
        """
        record_processor = CsvRecordProcessor(Account.WAON.value)
        with pytest.raises(InvalidRecordError) as excinfo:
            record_processor.execute(["2018/11/11", "板橋前野町", "5,000円", "オートチャージ", "-"])
        exception = excinfo.value
        assert len(exception.list_error) == 1
        assert str(exception.list_error[0]) == "Charge kind in charge row is required. Charge kind = -"
        assert not exception.undefined_content_error_handler.is_presented