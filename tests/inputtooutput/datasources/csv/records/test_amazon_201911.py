"""Tests for AmazonRow."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.records.amazon_201911 import (
    Amazon201911DiscountRow,
    Amazon201911PaymentRow,
    Amazon201911ShippingHandlingRow,
)
from zaimcsvconverter.models import Item, Store


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
