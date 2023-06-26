"""Tests for sf_card_viewer.py."""
from datetime import datetime

from pydantic import ValidationError
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.datasources.csv.data import RowDataFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.sf_card_viewer import SFCardViewerRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.sf_card_viewer import (
    SFCardViewerEnterExitRow,
    SFCardViewerEnterRow,
    SFCardViewerRow,
)
from zaimcsvconverter.models import Store


class TestSFCardViewerRow:
    """Tests for SFCardViewerRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_sf_card_viewer")
    def test_init() -> None:
        """Arguments should set into properties."""
        sf_card_viewer_row = SFCardViewerEnterRow(
            InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION,
            CONFIG.pasmo,
        )
        # Reason: Time is not used in this process.
        assert sf_card_viewer_row.date == datetime(2018, 11, 13, 0, 0, 0)  # noqa: DTZ001
        assert isinstance(sf_card_viewer_row.store, Store)
        assert sf_card_viewer_row.store.name_zaim == "東京地下鉄株式会社　南北線後楽園駅"


class TestSFCardViewerSalesGoodsRow:
    """Tests for SFCardViewerSalesGoodsRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        ("_yaml_config_load", "expected"),
        [("config_skip_sales_goods_row.yml.dist", True), ("config_not_skip_sales_goods_row.yml.dist", False)],
        indirect=["_yaml_config_load"],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_sf_card_viewer")
    def test_is_row_to_skip(*, expected: bool) -> None:
        """SFCardViewerSalesGoodsRow should convert to ZaimPaymentRow."""
        sf_card_viewer_row = SFCardViewerRow(InstanceResource.ROW_DATA_SF_CARD_VIEWER_SALES_GOODS, CONFIG.pasmo)
        assert sf_card_viewer_row.is_row_to_skip == expected


class TestSFCardViewerExitByWindowRow:
    """Tests for SFCardViewerTransportationRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        ("sf_card_viewer_row_data", "expected"),
        [
            (
                InstanceResource.SF_CARD_VIEWER_ROW_DATA_FACTORY.create(
                    ["2018/11/25", "", "東武", "北千住", "", "JR東", "北千住", "0", "2621", "窓出"],
                ),
                False,
            ),
            (
                InstanceResource.SF_CARD_VIEWER_ROW_DATA_FACTORY.create(
                    ["2018/11/25", "", "東武", "とうきょうスカイツリー", "", "東武", "北千住", "0", "2621", "窓出"],
                ),
                False,
            ),
            (
                InstanceResource.SF_CARD_VIEWER_ROW_DATA_FACTORY.create(
                    ["2018/11/25", "", "東武", "北千住", "", "東武", "北千住", "100", "2621", "窓出"],
                ),
                False,
            ),
            (InstanceResource.ROW_DATA_SF_CARD_VIEWER_EXIT_BY_WINDOW_KITASENJU_STATION, True),
        ],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_sf_card_viewer")
    def test_is_row_to_skip(sf_card_viewer_row_data: SFCardViewerRowData, *, expected: bool) -> None:
        """Method should return true when entered station is as same as exit station and used amount is 0."""
        sf_card_viewer_row = SFCardViewerEnterExitRow(sf_card_viewer_row_data, CONFIG.pasmo)
        assert sf_card_viewer_row.is_row_to_skip == expected

    @staticmethod
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_sf_card_viewer")
    def test_create_fail() -> None:
        """Method should raise ValueError when note is not defined."""
        with pytest.raises(ValidationError) as excinfo:
            # pylint: disable=protected-access
            RowDataFactory(SFCardViewerRowData).create(InstanceResource.ROW_DATA_SF_CARD_VIEWER_UNSUPPORTED_NOTE)
        assert len(excinfo.value.errors()) == 1
        error = excinfo.value.errors()[0]
        assert error["loc"] == ("note",)
        assert error["msg"] == "".join(
            ["value is not a valid enumeration member; permitted: '', '物販', 'ｵｰﾄﾁｬｰｼﾞ', '窓出', 'ﾊﾞｽ/路面等'"],
        )
