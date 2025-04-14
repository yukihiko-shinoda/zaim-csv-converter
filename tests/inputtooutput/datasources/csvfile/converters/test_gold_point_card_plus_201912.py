"""Test for GoldPointCardPlus201912RowFactory."""

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912RowFactory,
)
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912RowData,
)
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912Row,
)


class TestGoldPointCardPlus201912RowFactory:
    """Tests for GoldPointCardPlusRowFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        ("argument", "expected"),
        [(InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_TOKYO_ELECTRIC, GoldPointCardPlus201912Row)],
    )
    @pytest.mark.usefixtures("database_session_stores_gold_point_card_plus")
    def test_create(argument: GoldPointCardPlus201912RowData, expected: type[GoldPointCardPlus201912Row]) -> None:
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        gold_point_card_plus_row = GoldPointCardPlus201912RowFactory().create(argument)
        assert isinstance(gold_point_card_plus_row, expected)
