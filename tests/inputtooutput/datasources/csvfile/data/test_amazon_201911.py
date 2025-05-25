"""Tests for AmazonRow."""

from datetime import datetime

from tests.testlibraries.assert_list import assert_each_properties
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import RowDataFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.amazon_201911 import Amazon201911RowData


# Reason: Unluckily duplicate specification with Amazon. pylint: disable=duplicate-code
class TestAmazon201911RowData:
    """Tests for AmazonRowData."""

    # Reason: Testing different version of row data is better to be separated code.
    # noinspection DuplicatedCode
    @staticmethod
    def test_init_and_property() -> None:  # pylint: disable=too-many-locals
        """Tests following:

        - Property date should return datetime object.
        - Property store_date should return used_store.
        """
        ordered_date = "2018/10/23"
        order_id = "123-4567890-1234567"
        item_name = "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト"
        note = "販売： Amazon Japan G.K.  コンディション： 新品"  # noqa: RUF001
        price = "4980"
        number = "1"
        subtotal_price_item = "6276"
        total_order = "6390"
        destination = "ローソン桜塚"
        status = "2018年10月23日に発送済み"
        billing_address = "テストアカウント"
        billing_amount = "5952"
        credit_card_billing_date = "2018/10/23"
        credit_card_billing_amount = "5952"
        credit_card_identity = "Visa（下4けたが1234）"  # noqa: RUF001
        url_order_summary = "https://www.amazon.co.jp/gp/css/summary/edit.html?ie=UTF8&orderID=123-4567890-1234567"
        url_receipt = (
            "https://www.amazon.co.jp/gp/css/summary/print.html/ref=oh_aui_ajax_dpi"
            "?ie=UTF8&orderID=123-4567890-1234567"
        )
        url_item = "https://www.amazon.co.jp/gp/product/B06ZYTTC4P/ref=od_aui_detailpages01?ie=UTF8&psc=1"
        expected_price = 4980
        expected_subtotal_price_item = 6276
        expected_total_order = 6390
        expected_billing_amount = 5952
        row_data = RowDataFactory(Amazon201911RowData).create(
            [
                ordered_date,
                order_id,
                item_name,
                note,
                price,
                number,
                subtotal_price_item,
                total_order,
                destination,
                status,
                billing_address,
                billing_amount,
                credit_card_billing_date,
                credit_card_billing_amount,
                credit_card_identity,
                url_order_summary,
                url_receipt,
                url_item,
            ],
        )
        assert_each_properties(
            row_data,
            [
                # Reason: Time is not used in this process.
                datetime(2018, 10, 23, 0, 0),  # noqa: DTZ001
                order_id,
                item_name,
                note,
                expected_price,
                1,
                expected_subtotal_price_item,
                expected_total_order,
                destination,
                status,
                billing_address,
                expected_billing_amount,
                credit_card_billing_date,
                credit_card_billing_amount,
                credit_card_identity,
                url_order_summary,
                url_receipt,
                url_item,
            ],
        )
