"""Test for SFCardViewerRowFactory."""
from dataclasses import dataclass

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.datasources.csv.converters.sf_card_viewer import SFCardViewerRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.sf_card_viewer import SFCardViewerRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.sf_card_viewer import SFCardViewerRow


@dataclass
class Expected:
    """Expected values."""

    is_transportation: bool
    is_sales_goods: bool
    is_auto_charge: bool
    is_exit_by_window: bool
    is_bus_tram: bool


class TestSFCardViewerRowFactory:
    """Tests for SFCardViewerRowFactory."""

    # pylint: disable=unused-argument,too-many-arguments
    @pytest.mark.parametrize(
        ("argument", "expected"),
        [
            (
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION,
                Expected(
                    is_transportation=True,
                    is_sales_goods=False,
                    is_auto_charge=False,
                    is_exit_by_window=False,
                    is_bus_tram=False,
                ),
            ),
            (
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_SALES_GOODS,
                Expected(
                    is_transportation=False,
                    is_sales_goods=True,
                    is_auto_charge=False,
                    is_exit_by_window=False,
                    is_bus_tram=False,
                ),
            ),
            (
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_AUTO_CHARGE_AKIHABARA_STATION,
                Expected(
                    is_transportation=False,
                    is_sales_goods=False,
                    is_auto_charge=True,
                    is_exit_by_window=False,
                    is_bus_tram=False,
                ),
            ),
            (
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_EXIT_BY_WINDOW_KITASENJU_STATION,
                Expected(
                    is_transportation=False,
                    is_sales_goods=False,
                    is_auto_charge=False,
                    is_exit_by_window=True,
                    is_bus_tram=False,
                ),
            ),
            (
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_BUS_TRAM,
                Expected(
                    is_transportation=False,
                    is_sales_goods=False,
                    is_auto_charge=False,
                    is_exit_by_window=False,
                    is_bus_tram=True,
                ),
            ),
        ],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_sf_card_viewer")
    def test_create_success(self, argument: SFCardViewerRowData, expected: Expected) -> None:
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        sf_card_viewer_row = SFCardViewerRowFactory(lambda: CONFIG.pasmo).create(argument)
        assert isinstance(sf_card_viewer_row, SFCardViewerRow)
        self.assert_properties1(sf_card_viewer_row, expected)
        self.assert_properties2(sf_card_viewer_row, expected)

    def assert_properties1(self, sf_card_viewer_row: SFCardViewerRow, expected: Expected) -> None:
        assert sf_card_viewer_row.is_transportation == expected.is_transportation
        assert sf_card_viewer_row.is_sales_goods == expected.is_sales_goods
        assert sf_card_viewer_row.is_auto_charge == expected.is_auto_charge

    def assert_properties2(self, sf_card_viewer_row: SFCardViewerRow, expected: Expected) -> None:
        assert sf_card_viewer_row.is_exit_by_window == expected.is_exit_by_window
        assert sf_card_viewer_row.is_bus_tram == expected.is_bus_tram
