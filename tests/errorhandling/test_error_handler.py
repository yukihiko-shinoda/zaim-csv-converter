"""Tests for error_handler.py."""
from typing import ClassVar

import pytest

from tests.testlibraries.assert_list import assert_list
from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.errorhandling.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.inputtooutput.datasources.csv.records.amazon import AmazonRow
from zaimcsvconverter.inputtooutput.datasources.csv.records.waon import WaonRow


class TestErrorHandler:
    """Tests for UndefinedContentErrorHandler."""

    ERROR_WAON: ClassVar[list[str]] = ["waon.csv", "ファミリーマートかぶと町永代", ""]
    ERROR_AMAZON: ClassVar[list[str]] = [
        "amazon.csv",
        "",
        "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト",
    ]

    @staticmethod
    def test_init_is_presented_false() -> None:
        """list_error should be empty when initialized."""
        assert not UndefinedContentErrorHandler().is_presented

    @pytest.mark.usefixtures("_yaml_config_load", "database_session_with_schema")
    def test_single_error(self) -> None:
        error_handler = UndefinedContentErrorHandler()
        error_handler.extend_list(self.create_waon_row_report_undefined_content_error())
        assert error_handler.list_error == [self.ERROR_WAON]

    @pytest.mark.usefixtures("_yaml_config_load", "database_session_with_schema")
    def test_same_error(self) -> None:
        error_handler = UndefinedContentErrorHandler()
        error_handler.extend_list(self.create_amazon_row_report_undefined_content_error())
        error_handler.extend_list(self.create_amazon_row_report_undefined_content_error())
        assert error_handler.list_error == [self.ERROR_AMAZON]

    @pytest.mark.usefixtures("_yaml_config_load", "database_session_with_schema")
    def test_append_undefined_content_extend_is_presented_true_uniquify_iter(self) -> None:
        """Instance should be iterable."""
        error_handler_a = UndefinedContentErrorHandler()
        error_handler_a.extend_list(self.create_waon_row_report_undefined_content_error())
        error_handler_b = UndefinedContentErrorHandler()
        error_handler_b.extend_list(self.create_amazon_row_report_undefined_content_error())
        error_handler_b.extend_list(self.create_amazon_row_report_undefined_content_error())
        error_handler_a.extend(error_handler_b)
        list_expected_error = [self.ERROR_AMAZON, self.ERROR_WAON]
        assert error_handler_a.list_error == list_expected_error
        assert error_handler_a.is_presented
        error_handler_a.uniquify()
        assert_list(error_handler_a, list_expected_error)

    def create_waon_row_report_undefined_content_error(self) -> list[list[str]]:
        waon_row = WaonRow(InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI)
        # Reason: To update state. pylint: disable=pointless-statement
        waon_row.validate  # noqa: B018
        return waon_row.get_report_undefined_content_error()

    def create_amazon_row_report_undefined_content_error(self) -> list[list[str]]:
        amazon_row = AmazonRow(InstanceResource.ROW_DATA_AMAZON_ECHO_DOT)
        # Reason: To update state. pylint: disable=pointless-statement
        amazon_row.validate  # noqa: B018
        return amazon_row.get_report_undefined_content_error()
