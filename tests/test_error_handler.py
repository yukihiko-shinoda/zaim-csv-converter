"""Tests for error_handler.py."""
from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.account import FileNameCsvConvert
from zaimcsvconverter.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.inputcsvformats.amazon import AmazonRow
from zaimcsvconverter.inputcsvformats.waon import WaonRow
from zaimcsvconverter.models import AccountId


class TestErrorHandler:
    """Tests for UndefinedContentErrorHandler"""
    @staticmethod
    def test_init_is_presented_false():
        """list_error should be empty when initialized."""
        assert not UndefinedContentErrorHandler().is_presented

    # pylint: disable=unused-argument
    @staticmethod
    def test_append_undefined_content_extend_is_presented_true_uniquify_iter(yaml_config_load):
        """Instance should be iterable."""
        error_amazon = ['amazon.csv', '', 'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト']
        error_waon = ['waon.csv', 'ファミリーマートかぶと町永代', '']
        error_handler_a = UndefinedContentErrorHandler()
        error_handler_a.append(
            FileNameCsvConvert.WAON,
            WaonRow(AccountId.WAON, InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI)
        )
        assert error_handler_a.list_error == [error_waon]
        error_handler_b = UndefinedContentErrorHandler()
        error_handler_b.append(
            FileNameCsvConvert.AMAZON, AmazonRow(AccountId.AMAZON, InstanceResource.ROW_DATA_AMAZON_ECHO_DOT)
        )
        error_handler_b.append(
            FileNameCsvConvert.AMAZON, AmazonRow(AccountId.AMAZON, InstanceResource.ROW_DATA_AMAZON_ECHO_DOT)
        )
        assert error_handler_b.list_error == [error_amazon, error_amazon]
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
