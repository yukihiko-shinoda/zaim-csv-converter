"""Test for GoldPointCardPlusRowFactory."""

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.converters.gold_point_card_plus import GoldPointCardPlusRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.gold_point_card_plus import GoldPointCardPlusRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.gold_point_card_plus import GoldPointCardPlusRow


class TestGoldPointCardPlusRowFactory:
    """Tests for GoldPointCardPlusRowFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        ("argument", "expected"),
        [(InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC, GoldPointCardPlusRow)],
    )
    @pytest.mark.usefixtures("database_session_stores_gold_point_card_plus")
    def test_create(argument: GoldPointCardPlusRowData, expected: type[GoldPointCardPlusRow]) -> None:
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        gold_point_card_plus_row = GoldPointCardPlusRowFactory().create(argument)
        assert isinstance(gold_point_card_plus_row, expected)
