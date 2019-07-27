"""Tests for amazon.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.inputcsvformats.amazon import AmazonRowFactory, AmazonRow
from zaimcsvconverter.models import AccountId
from zaimcsvconverter.zaim_row import ZaimPaymentRow
from zaimcsvconverter.rowconverters.amazon import AmazonZaimPaymentRowConverter, AmazonZaimRowConverterSelector


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
        amazon_row = AmazonRow(AccountId.AMAZON, InstanceResource.ROW_DATA_AMAZON_ECHO_DOT)
        zaim_row = AmazonZaimPaymentRowConverter(amazon_row).convert()
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == '2018-10-23'
        assert zaim_row_data.store_name == store_name
        assert zaim_row_data.item_name == item_name
        assert zaim_row_data.cash_flow_source == config_account_name
        assert zaim_row_data.note == ''
        assert zaim_row_data.amount_payment == expected_amount


class TestAmazonZaimRowConverterSelector:
    """Tests for AmazonZaimRowConverterSelector."""
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
        input_row = AmazonRowFactory().create(AccountId.AMAZON, input_row_data)
        assert AmazonZaimRowConverterSelector().select(input_row) == expected
