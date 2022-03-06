"""Tests for AmazonRow."""
from datetime import datetime

from zaimcsvconverter.inputtooutput.datasources.csv.data.amazon_201911 import Amazon201911RowData
from zaimcsvconverter.inputtooutput.datasources.csv.data import RowDataFactory


class TestAmazon201911RowData:
    """Tests for AmazonRowData."""

    # Reason: Testing different version of row data is better to be separated code.
    # noinspection DuplicatedCode
    @staticmethod
    # pylint: disable=too-many-locals
    def test_init_and_property() -> None:
        """Tests following:

        - Property date should return datetime object.
        - Property store_date should return used_store.
        """
        ordered_date = "2018/10/23"
        order_id = "123-4567890-1234567"
        item_name = "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト"
        note = "販売： Amazon Japan G.K.  コンディション： 新品"
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
        credit_card_identity = "Visa（下4けたが1234）"
        url_order_summary = "https://www.amazon.co.jp/gp/css/summary/edit.html?ie=UTF8&orderID=123-4567890-1234567"
        url_receipt = (
            "https://www.amazon.co.jp/gp/css/summary/print.html/ref=oh_aui_ajax_dpi"
            "?ie=UTF8&orderID=123-4567890-1234567"
        )
        url_item = "https://www.amazon.co.jp/gp/product/B06ZYTTC4P/ref=od_aui_detailpages01?ie=UTF8&psc=1"
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
            ]
        )
        assert row_data.order_id == order_id
        assert row_data.note == note
        assert row_data.price == 4980
        assert row_data.number == 1
        assert row_data.subtotal_price_item == 6276
        assert row_data.destination == destination
        assert row_data.status == status
        assert row_data.billing_address == billing_address
        assert row_data.billing_amount == billing_amount
        assert row_data.credit_card_billing_date == credit_card_billing_date
        assert row_data.credit_card_billing_amount == credit_card_billing_amount
        assert row_data.credit_card_identity == credit_card_identity
        assert row_data.url_order_summary == url_order_summary
        assert row_data.url_receipt == url_receipt
        assert row_data.url_item == url_item
        assert row_data.date == datetime(2018, 10, 23, 0, 0)
        assert row_data.total_order == 6390
        assert row_data.item_name == item_name
