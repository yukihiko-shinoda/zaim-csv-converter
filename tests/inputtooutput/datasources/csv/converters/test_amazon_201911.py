"""Test for Amazon201911RowFactory."""

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.converters.amazon_201911 import Amazon201911RowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.amazon_201911 import Amazon201911RowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.amazon_201911 import (
    Amazon201911DiscountRow,
    Amazon201911ItemRow,
    Amazon201911PaymentRow,
    Amazon201911RowToSkip,
    Amazon201911ShippingHandlingRow,
)


class TestAmazon201911RowFactory:
    """Tests for AmazonRowFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        ("argument", "expected"),
        [
            (InstanceResource.ROW_DATA_AMAZON_201911_ECHO_DOT, Amazon201911PaymentRow),
            (InstanceResource.ROW_DATA_AMAZON_201911_AMAZON_POINT, Amazon201911DiscountRow),
            (InstanceResource.ROW_DATA_AMAZON_201911_SHIPPING_HANDLING, Amazon201911ShippingHandlingRow),
            (InstanceResource.ROW_DATA_AMAZON_201911_MS_Learn_IN_MANGA, Amazon201911RowToSkip),
        ],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_item")
    def test_create(argument: Amazon201911RowData, expected: type[Amazon201911ItemRow]) -> None:
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        gold_point_card_plus_row = Amazon201911RowFactory().create(argument)
        assert isinstance(gold_point_card_plus_row, expected)
