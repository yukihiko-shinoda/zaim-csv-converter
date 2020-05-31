"""Tests for amazon.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.inputcsvformats.amazon_201911 import Amazon201911RowFactory, Amazon201911RowData, \
    Amazon201911PaymentRow, Amazon201911DiscountRow
from zaimcsvconverter.rowconverters.amazon201911 import Amazon201911DiscountZaimPaymentRowConverter, \
    Amazon201911PaymentZaimPaymentRowConverter, Amazon201911ZaimRowConverterFactory
from zaimcsvconverter.zaim_row import ZaimPaymentRow, ZaimRowFactory


class TestAmazon201911DiscountZaimPaymentRowConverter:
    """ Tests for Amazon201911ZaimPaymentRowConverter."""
    # pylint: disable=unused-argument
    @staticmethod
    def test(yaml_config_load, database_session_item):
        """Arguments should set into properties."""
        expected_amount = -11
        config_account_name = 'ヨドバシゴールドポイントカード・プラス'
        store_name = 'Amazon Japan G.K.'
        item_name = '（Amazon ポイント）'
        amazon_row = Amazon201911DiscountRow(InstanceResource.ROW_DATA_AMAZON_201911_AMAZON_POINT)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(Amazon201911DiscountZaimPaymentRowConverter(amazon_row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == '2019-11-09'
        assert zaim_row_data.store_name == store_name
        assert zaim_row_data.item_name == item_name
        assert zaim_row_data.cash_flow_source == config_account_name
        assert zaim_row_data.note == ''
        assert zaim_row_data.amount_payment == expected_amount


class TestAmazon201911PaymentZaimPaymentRowConverter:
    """ Tests for Amazon201911ZaimPaymentRowConverter."""
    # pylint: disable=unused-argument
    @staticmethod
    def test(yaml_config_load, database_session_item):
        """Arguments should set into properties."""
        expected_amount = 4980
        config_account_name = 'ヨドバシゴールドポイントカード・プラス'
        store_name = 'Amazon Japan G.K.'
        item_name = 'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト'
        amazon_row = Amazon201911PaymentRow(InstanceResource.ROW_DATA_AMAZON_201911_ECHO_DOT)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(Amazon201911PaymentZaimPaymentRowConverter(amazon_row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == '2019-11-09'
        assert zaim_row_data.store_name == store_name
        assert zaim_row_data.item_name == item_name
        assert zaim_row_data.cash_flow_source == config_account_name
        assert zaim_row_data.note == ''
        assert zaim_row_data.amount_payment == expected_amount


class TestAmazon201911ZaimRowConverterFactory:
    """Tests for Amazon201911ZaimRowConverterFactory."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'database_session_with_schema, input_row_data, expected',
        [
            # Case when Amazon payment
            ([InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_ECHO_DOT], InstanceResource.ROW_DATA_AMAZON_201911_ECHO_DOT,
             Amazon201911PaymentZaimPaymentRowConverter),
            # Case when Amazon discount
            ([InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_AMAZON_POINT],
             InstanceResource.ROW_DATA_AMAZON_201911_AMAZON_POINT,
             Amazon201911DiscountZaimPaymentRowConverter),
        ], indirect=['database_session_with_schema']
    )
    def test(yaml_config_load, database_session_with_schema, input_row_data: Amazon201911RowData, expected):
        """Input row should convert to suitable ZaimRow by transfer target."""
        input_row = Amazon201911RowFactory().create(input_row_data)
        assert isinstance(Amazon201911ZaimRowConverterFactory().create(input_row), expected)
