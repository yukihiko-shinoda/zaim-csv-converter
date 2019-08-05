"""Tests for row_processror.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.account import Account
from zaimcsvconverter.exceptions import InvalidRowError
from zaimcsvconverter.row_processor import RowProcessor


class TestRowProcessor:
    """Tests for RowProcessor."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'database_session_with_schema',
        [[InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO]],
        indirect=['database_session_with_schema']
    )
    def test(yaml_config_load, database_session_with_schema):
        """
        RowProcessor should raise error when input row is invalid.
        RowProcessor should collect error when input row is invalid.
        """
        row_process = RowProcessor(Account.WAON)
        with pytest.raises(InvalidRowError):
            row_process.execute(['2018/11/11', '板橋前野町', '5,000円', 'オートチャージ', '-'])
        list_error = row_process.list_error
        assert len(list_error) == 1
        assert str(list_error[0]) == 'Charge kind in charge row is required. Charge kind = ChargeKind.NULL'
        assert not row_process.undefined_content_error_handler.is_presented
