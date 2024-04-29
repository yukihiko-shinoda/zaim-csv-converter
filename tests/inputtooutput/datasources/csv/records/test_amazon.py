"""Tests for AmazonRow."""

from datetime import datetime

import pytest

from tests.testlibraries.assert_list import assert_each_properties
from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.records.amazon import AmazonRow
from zaimcsvconverter.models import Item, Store


class TestAmazonRow:
    """Tests for AmazonRow."""

    @pytest.mark.usefixtures("_yaml_config_load", "database_session_item")
    def test_init(self) -> None:
        """Arguments should set into properties."""
        expected_price = 4980
        store_name = ""
        store_name_zaim = "Amazon Japan G.K."
        item_name = "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト"
        amazon_row = AmazonRow(InstanceResource.ROW_DATA_AMAZON_ECHO_DOT)
        assert_each_properties(
            amazon_row,
            [
                [],
                # Reason: Time is not used in this process.
                datetime(2018, 10, 23, 0, 0, 0),  # noqa: DTZ001
                store_name,
                item_name,
                None,
                expected_price,
                1,
            ],
        )
        self.assert_store_and_item(amazon_row, store_name_zaim, item_name)

    def assert_store_and_item(self, amazon_row: AmazonRow, store_name_zaim: str, item_name: str) -> None:
        assert isinstance(amazon_row.store, Store)
        assert amazon_row.store.name_zaim == store_name_zaim
        assert isinstance(amazon_row.item, Item)
        assert amazon_row.item.name == item_name
