"""Test for SFCardViewerRowFactory."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.datasources.csv.converters.sf_card_viewer import SFCardViewerRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.sf_card_viewer import SFCardViewerRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.sf_card_viewer import SFCardViewerRow


class TestSFCardViewerRowFactory:
    """Tests for SFCardViewerRowFactory."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        (
            "argument",
            "expected_is_transportation",
            "expected_is_sales_goods",
            "expected_is_auto_charge",
            "expected_is_exit_by_window",
            "expected_is_bus_tram",
        ),
        [
            (
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION,
                True,
                False,
                False,
                False,
                False,
            ),
            (InstanceResource.ROW_DATA_SF_CARD_VIEWER_SALES_GOODS, False, True, False, False, False),
            (InstanceResource.ROW_DATA_SF_CARD_VIEWER_AUTO_CHARGE_AKIHABARA_STATION, False, False, True, False, False),
            (
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_EXIT_BY_WINDOW_KITASENJU_STATION,
                False,
                False,
                False,
                True,
                False,
            ),
            (InstanceResource.ROW_DATA_SF_CARD_VIEWER_BUS_TRAM, False, False, False, False, True),
        ],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_sf_card_viewer")
    def test_create_success(  # noqa: PLR0913
        argument: SFCardViewerRowData,
        *,
        expected_is_transportation: bool,
        expected_is_sales_goods: bool,
        expected_is_auto_charge: bool,
        expected_is_exit_by_window: bool,
        expected_is_bus_tram: bool,
    ) -> None:
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        sf_card_viewer_row = SFCardViewerRowFactory(lambda: CONFIG.pasmo).create(argument)
        assert isinstance(sf_card_viewer_row, SFCardViewerRow)
        assert sf_card_viewer_row.is_transportation == expected_is_transportation
        assert sf_card_viewer_row.is_sales_goods == expected_is_sales_goods
        assert sf_card_viewer_row.is_auto_charge == expected_is_auto_charge
        assert sf_card_viewer_row.is_exit_by_window == expected_is_exit_by_window
        assert sf_card_viewer_row.is_bus_tram == expected_is_bus_tram
