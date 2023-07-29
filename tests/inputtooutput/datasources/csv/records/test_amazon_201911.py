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
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_item")
    def test_init(self) -> None:
        """Arguments should set into properties."""
        store_name = "Amazon Japan G.K."
        item_name = "（Amazon ポイント）"  # noqa: RUF001
        amazon_row = Amazon201911DiscountRow(InstanceResource.ROW_DATA_AMAZON_201911_AMAZON_POINT)
        # Reason: Time is not used in this process.
        assert amazon_row.date == datetime(2019, 11, 9, 0, 0, 0)  # noqa: DTZ001
        self.assert_store_and_item(amazon_row, store_name, item_name)

    def assert_store_and_item(self, amazon_row: Amazon201911DiscountRow, store_name: str, item_name: str) -> None:
        assert isinstance(amazon_row.store, Store)
        assert amazon_row.store.name_zaim == store_name
        assert isinstance(amazon_row.item, Item)
        assert amazon_row.item.name == item_name

    @staticmethod
    def test_total_order_fail() -> None:
        """Property should raise ValueError when value is None."""
        with pytest.raises(ValueError, match=r"Total\sorder\son\sdiscount\srow\sis\snot\sallowed\sempty\."):
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            Amazon201911DiscountRow(InstanceResource.ROW_DATA_AMAZON_201911_HUMMING_FINE).total_order  # noqa: B018


class TestAmazon201911ShippingHandlingRow:
    """Tests for Amazon201911ShippingHandlingRow."""

    @staticmethod
    def test_subtotal_price_item_fail() -> None:
        """Property should raise ValueError when subtotal price item is None."""
        with pytest.raises(
            ValueError,
            match=r"Subtotal\sprice\sitem\son\sshipping\shandling\srow\sis\snot\sallowed\sempty\.",
        ):
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            Amazon201911ShippingHandlingRow(  # noqa: B018
                InstanceResource.ROW_DATA_AMAZON_201911_HUMMING_FINE,
            ).subtotal_price_item


class TestAmazon201911PaymentRow:
    """Tests for Amazon201911PaymentRow."""

    # Reason: Testing different version of row data is better to be separated code.
    # noinspection DuplicatedCode
    # pylint: disable=unused-argument
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_item")
    def test_init(self) -> None:
        """Arguments should set into properties."""
        expected_price = 4980
        store_name = "Amazon Japan G.K."
        item_name = "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト"
        amazon_row = Amazon201911PaymentRow(InstanceResource.ROW_DATA_AMAZON_201911_ECHO_DOT)
        assert amazon_row.price == expected_price
        assert amazon_row.number == 1
        # Reason: Time is not used in this process.
        assert amazon_row.date == datetime(2019, 11, 9, 0, 0, 0)  # noqa: DTZ001
        self.assert_store_and_item(amazon_row, store_name, item_name)

    def assert_store_and_item(self, amazon_row: Amazon201911PaymentRow, store_name: str, item_name: str) -> None:
        assert isinstance(amazon_row.store, Store)
        assert amazon_row.store.name_zaim == store_name
        assert isinstance(amazon_row.item, Item)
        assert amazon_row.item.name == item_name

    @staticmethod
    def test_price_fail() -> None:
        """Property should raise ValueError when value is None."""
        with pytest.raises(ValueError, match=r"Price\son\spayment\srow\sis\snot\sallowed\sempty\."):
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            Amazon201911PaymentRow(InstanceResource.ROW_DATA_AMAZON_201911_AMAZON_POINT).price  # noqa: B018

    @staticmethod
    def test_number_fail() -> None:
        """Property should raise ValueError when value is None."""
        with pytest.raises(ValueError, match=r"Number\son\spayment\srow\sis\snot\sallowed\sempty\."):
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            Amazon201911PaymentRow(InstanceResource.ROW_DATA_AMAZON_201911_AMAZON_POINT).number  # noqa: B018
