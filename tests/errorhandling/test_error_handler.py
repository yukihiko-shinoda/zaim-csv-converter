"""Tests for error_handler.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.errorhandling.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.inputtooutput.datasources.csv.records.amazon import AmazonRow
from zaimcsvconverter.inputtooutput.datasources.csv.records.waon import WaonRow


class TestErrorHandler:
    """Tests for UndefinedContentErrorHandler."""

    @staticmethod
    def test_init_is_presented_false() -> None:
        """list_error should be empty when initialized."""
        assert not UndefinedContentErrorHandler().is_presented

    @staticmethod
    # pylint: disable=unused-argument
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test_append_undefined_content_extend_is_presented_true_uniquify_iter() -> None:
        """Instance should be iterable."""
        error_amazon = ["amazon.csv", "", "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト"]
        error_waon = ["waon.csv", "ファミリーマートかぶと町永代", ""]
        error_handler_a = UndefinedContentErrorHandler()
        waon_row = WaonRow(InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI)
        # Reason: To update state. pylint: disable=pointless-statement
        waon_row.validate
        error_handler_a.extend_list(waon_row.get_report_undefined_content_error())
        assert error_handler_a.list_error == [error_waon]
        error_handler_b = UndefinedContentErrorHandler()
        amazon_row_1 = AmazonRow(InstanceResource.ROW_DATA_AMAZON_ECHO_DOT)
        # Reason: To update state. pylint: disable=pointless-statement
        amazon_row_1.validate
        error_handler_b.extend_list(amazon_row_1.get_report_undefined_content_error())
        amazon_row_2 = AmazonRow(InstanceResource.ROW_DATA_AMAZON_ECHO_DOT)
        # Reason: To update state. pylint: disable=pointless-statement
        amazon_row_2.validate
        error_handler_b.extend_list(amazon_row_2.get_report_undefined_content_error())
        assert error_handler_b.list_error == [error_amazon]
        error_handler_a.extend(error_handler_b)
        assert error_handler_a.list_error == [error_amazon, error_waon]
        assert error_handler_a.is_presented
        error_handler_a.uniquify()
        list_error = [error_amazon, error_waon]
        index = 0
        for error_row in error_handler_a:
            assert error_row == list_error[index]
            index += 1
        assert index == 2
