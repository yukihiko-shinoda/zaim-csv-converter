"""Test for ViewCardRowFactory."""

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.view_card import ViewCardRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.view_card import ViewCardRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.view_card import ViewCardStoreRow


class TestViewCardRowFactory:
    """Tests for GoldPointCardPlusRowFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        ("argument", "expected"),
        [(InstanceResource.ROW_DATA_VIEW_CARD_ANNUAL_FEE, ViewCardStoreRow)],
    )
    @pytest.mark.usefixtures("database_session_stores_view_card")
    def test_create(argument: ViewCardRowData, expected: type[ViewCardStoreRow]) -> None:
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        view_card_row = ViewCardRowFactory().create(argument)
        assert isinstance(view_card_row, expected)
