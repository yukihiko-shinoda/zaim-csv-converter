"""Tests for amazon.py."""
from pathlib import Path

import pytest

from tests.testlibraries.assert_list import assert_each_properties
from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimPaymentRow


class TestAmazonZaimPaymentRowConverter:
    """Tests for AmazonZaimPaymentRowConverter."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_item")
    def test() -> None:
        """Arguments should set into properties."""
        expected_amount = 4980
        config_account_name = "ヨドバシゴールドポイントカード・プラス"
        store_name = "Amazon Japan G.K."
        item_name = "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト"
        note = ""
        account_context = Account.AMAZON.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        amazon_row = csv_record_processor.create_input_row_instance(InstanceResource.ROW_DATA_AMAZON_ECHO_DOT)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(amazon_row, Path()))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert_each_properties(
            zaim_row_data,
            ["2018-10-23", config_account_name, item_name, note, store_name, expected_amount],
            attribute_filter=["date", "cash_flow_source", "item_name", "note", "store_name", "amount_payment"],
        )
