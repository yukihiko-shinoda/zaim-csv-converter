"""Tests for amazon.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.inputcsvformats.amazon import AmazonRowFactory, AmazonRow
from zaimcsvconverter.models import FileCsvConvertId
from zaimcsvconverter.zaim_row import ZaimPaymentRow, ZaimRowFactory
from zaimcsvconverter.rowconverters.amazon import AmazonZaimPaymentRowConverter, AmazonZaimRowConverterFactory


class TestAmazonZaimPaymentRowConverter:
    """ Tests for AmazonZaimPaymentRowConverter."""
    # pylint: disable=unused-argument
    @staticmethod
    def test(yaml_config_load, database_session_item):
        """Arguments should set into properties."""
        expected_amount = 4980
        config_account_name = 'ヨドバシゴールドポイントカード・プラス'
        store_name = 'Amazon Japan G.K.'
        item_name = 'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト'
        amazon_row = AmazonRow(InstanceResource.ROW_DATA_AMAZON_ECHO_DOT)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(AmazonZaimPaymentRowConverter(amazon_row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == '2018-10-23'
        assert zaim_row_data.store_name == store_name
        assert zaim_row_data.item_name == item_name
        assert zaim_row_data.cash_flow_source == config_account_name
        assert zaim_row_data.note == ''
        assert zaim_row_data.amount_payment == expected_amount


class TestAmazonZaimRowConverterFactory:
    """Tests for AmazonZaimRowConverterFactory."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'database_session_with_schema, input_row_data, expected',
        [
            # Case when Amazon payment
            ([InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_ECHO_DOT], InstanceResource.ROW_DATA_AMAZON_ECHO_DOT,
             AmazonZaimPaymentRowConverter),
        ], indirect=['database_session_with_schema']
    )
    def test(yaml_config_load, database_session_with_schema, input_row_data, expected):
        """Input row should convert to suitable ZaimRow by transfer target."""
        input_row = AmazonRowFactory().create(input_row_data)
        assert isinstance(AmazonZaimRowConverterFactory().create(input_row), expected)
