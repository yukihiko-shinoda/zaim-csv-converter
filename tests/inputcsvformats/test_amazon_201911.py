"""Tests for AmazonRow."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputcsvformats.amazon_201911 import (
    Amazon201911DiscountRow,
    Amazon201911PaymentRow,
    Amazon201911RowData,
    Amazon201911ShippingHandlingRow,
)
from zaimcsvconverter.inputcsvformats import RowDataFactory
from zaimcsvconverter.models import Item, Store


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


class TestAmazon201911DiscountRow:
    """Tests for Amazon201911DiscountRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_item")
    def test_init() -> None:
        """Arguments should set into properties."""
        store_name = "Amazon Japan G.K."
        item_name = "（Amazon ポイント）"
        amazon_row = Amazon201911DiscountRow(InstanceResource.ROW_DATA_AMAZON_201911_AMAZON_POINT)
        assert amazon_row.date == datetime(2019, 11, 9, 0, 0, 0)
        assert isinstance(amazon_row.store, Store)
        assert amazon_row.store.name_zaim == store_name
        assert isinstance(amazon_row.item, Item)
        assert amazon_row.item.name == item_name

    @staticmethod
    def test_total_order_fail() -> None:
        """Property should raise ValueError when value is None."""
        with pytest.raises(ValueError) as error:
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            Amazon201911DiscountRow(InstanceResource.ROW_DATA_AMAZON_201911_HUMMING_FINE).total_order
        assert str(error.value) == "Total order on discount row is not allowed empty."


class TestAmazon201911ShippingHandlingRow:
    """Tests for Amazon201911ShippingHandlingRow."""

    @staticmethod
    def test_subtotal_price_item_fail() -> None:
        with pytest.raises(ValueError) as error:
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            Amazon201911ShippingHandlingRow(InstanceResource.ROW_DATA_AMAZON_201911_HUMMING_FINE).subtotal_price_item
        assert str(error.value) == "Subtotal price item on shipping handling row is not allowed empty."


class TestAmazon201911PaymentRow:
    """Tests for Amazon201911PaymentRow."""

    # Reason: Testing different version of row data is better to be separated code.
    # noinspection DuplicatedCode
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_item")
    def test_init() -> None:
        """Arguments should set into properties."""
        store_name = "Amazon Japan G.K."
        item_name = "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト"
        amazon_row = Amazon201911PaymentRow(InstanceResource.ROW_DATA_AMAZON_201911_ECHO_DOT)
        assert amazon_row.price == 4980
        assert amazon_row.number == 1
        assert amazon_row.date == datetime(2019, 11, 9, 0, 0, 0)
        assert isinstance(amazon_row.store, Store)
        assert amazon_row.store.name_zaim == store_name
        assert isinstance(amazon_row.item, Item)
        assert amazon_row.item.name == item_name

    @staticmethod
    def test_price_fail() -> None:
        """Property should raise ValueError when value is None."""
        with pytest.raises(ValueError) as error:
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            Amazon201911PaymentRow(InstanceResource.ROW_DATA_AMAZON_201911_AMAZON_POINT).price
        assert str(error.value) == "Price on payment row is not allowed empty."

    @staticmethod
    def test_number_fail() -> None:
        """Property should raise ValueError when value is None."""
        with pytest.raises(ValueError) as error:
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            Amazon201911PaymentRow(InstanceResource.ROW_DATA_AMAZON_201911_AMAZON_POINT).number
        assert str(error.value) == "Number on payment row is not allowed empty."
