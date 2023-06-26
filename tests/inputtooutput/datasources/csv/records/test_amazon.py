"""Tests for AmazonRow."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.records.amazon import AmazonRow
from zaimcsvconverter.models import Item, Store


class TestAmazonRow:
    """Tests for AmazonRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_item")
    def test_init() -> None:
        """Arguments should set into properties."""
        expected_price = 4980
        store_name = "Amazon Japan G.K."
        item_name = "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト"
        amazon_row = AmazonRow(InstanceResource.ROW_DATA_AMAZON_ECHO_DOT)
        assert amazon_row.price == expected_price
        assert amazon_row.number == 1
        # Reason: Time is not used in this process.
        assert amazon_row.date == datetime(2018, 10, 23, 0, 0, 0)  # noqa: DTZ001
        assert isinstance(amazon_row.store, Store)
        assert amazon_row.store.name_zaim == store_name
        assert isinstance(amazon_row.item, Item)
        assert amazon_row.item.name == item_name
