"""Tests for amazon.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputcsvformats.amazon import AmazonRowData
from zaimcsvconverter.inputtooutput.converters.recordtozaim.amazon import AmazonZaimPaymentRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimPaymentRow


class TestAmazonZaimPaymentRowConverter:
    """Tests for AmazonZaimPaymentRowConverter."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_item")
    def test() -> None:
        """Arguments should set into properties."""
        expected_amount = 4980
        config_account_name = "ヨドバシゴールドポイントカード・プラス"
        store_name = "Amazon Japan G.K."
        item_name = "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト"
        account_context = Account.AMAZON.value
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        amazon_row = csv_record_processor.create_input_row_instance(InstanceResource.ROW_DATA_AMAZON_ECHO_DOT)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(amazon_row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == "2018-10-23"
        assert zaim_row_data.store_name == store_name
        assert zaim_row_data.item_name == item_name
        assert zaim_row_data.cash_flow_source == config_account_name
        assert zaim_row_data.note == ""
        assert zaim_row_data.amount_payment == expected_amount


class TestAmazonZaimRowConverterFactory:
    """Tests for AmazonZaimRowConverterFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema, input_row_data, expected",
        [
            # Case when Amazon payment
            (
                [InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_ECHO_DOT],
                InstanceResource.ROW_DATA_AMAZON_ECHO_DOT,
                AmazonZaimPaymentRowConverter,
            ),
        ],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test(input_row_data: AmazonRowData, expected: type[AmazonZaimPaymentRowConverter]) -> None:
        """Input row should convert to suitable ZaimRow by transfer target."""
        account_context = Account.AMAZON.value
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        amazon_row = csv_record_processor.create_input_row_instance(input_row_data)
        actual = account_context.zaim_row_converter_factory.create(amazon_row)
        assert isinstance(actual, expected)
