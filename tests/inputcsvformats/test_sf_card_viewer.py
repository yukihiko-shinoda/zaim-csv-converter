"""Tests for sf_card_viewer.py."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.sf_card_viewer import SFCardViewerRowFactory, SFCardViewerRowData, \
    SFCardViewerRow, SFCardViewerEnterExitRow, SFCardViewerEnterRow
from zaimcsvconverter.models import Store, AccountId


class TestSFCardViewerRowData:
    """Tests for SFCardViewerRowData."""

    @staticmethod
    def test_init_and_property():
        """
        Property date should return datetime object.
        Property store_date should return used_store.
        """
        used_date = '2018/11/13'
        is_commuter_pass_enter = ''
        railway_company_name_enter = 'メトロ'
        station_name_enter = '六本木一丁目'
        is_commuter_pass_exit = ''
        railway_company_name_exit = 'メトロ'
        station_name_exit = '後楽園'
        used_amount = '195'
        balance = '3601'
        note = ''
        sf_card_viewer_row_data = SFCardViewerRowData(used_date, is_commuter_pass_enter, railway_company_name_enter,
                                                      station_name_enter, is_commuter_pass_exit,
                                                      railway_company_name_exit, station_name_exit, used_amount,
                                                      balance, note)
        assert sf_card_viewer_row_data.is_commuter_pass_enter == is_commuter_pass_enter
        assert sf_card_viewer_row_data.railway_company_name_enter == railway_company_name_enter
        assert sf_card_viewer_row_data.station_name_enter == station_name_enter
        assert sf_card_viewer_row_data.is_commuter_pass_exit == is_commuter_pass_exit
        assert sf_card_viewer_row_data.railway_company_name_exit == railway_company_name_exit
        assert sf_card_viewer_row_data.used_amount == 195
        assert sf_card_viewer_row_data.balance == balance
        assert sf_card_viewer_row_data.note == SFCardViewerRowData.Note.EMPTY
        assert sf_card_viewer_row_data.date == datetime(2018, 11, 13, 0, 0)
        assert sf_card_viewer_row_data.store_name == station_name_exit


class TestSFCardViewerRow:
    """Tests for SFCardViewerRow."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_init(yaml_config_load, database_session_stores_sf_card_viewer):
        """
        Arguments should set into properties.
        """
        sf_card_viewer_row = SFCardViewerEnterRow(
            AccountId.PASMO, InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION, CONFIG.pasmo
        )
        assert sf_card_viewer_row.date == datetime(2018, 11, 13, 0, 0, 0)
        assert isinstance(sf_card_viewer_row.store, Store)
        assert sf_card_viewer_row.store.name_zaim == '東京地下鉄株式会社　南北線後楽園駅'


class TestSFCardViewerSalesGoodsRow:
    """Tests for SFCardViewerSalesGoodsRow."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'yaml_config_load, expected', [
            ('config_skip_sales_goods_row.yml.dist', True),
            ('config_not_skip_sales_goods_row.yml.dist', False),
        ], indirect=['yaml_config_load']
    )
    def test_is_row_to_skip(
            yaml_config_load, database_session_stores_sf_card_viewer, expected
    ):
        """SFCardViewerSalesGoodsRow should convert to ZaimPaymentRow."""
        sf_card_viewer_row = SFCardViewerRow(
            AccountId.PASMO, InstanceResource.ROW_DATA_SF_CARD_VIEWER_SALES_GOODS, CONFIG.pasmo
        )
        assert sf_card_viewer_row.is_row_to_skip == expected


class TestSFCardViewerExitByWindowRow:
    """Tests for SFCardViewerTransportationRow."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize('sf_card_viewer_row_data, expected', [
        (SFCardViewerRowData('2018/11/25', '', '東武', '北千住', '', 'JR東', '北千住', '0', '2621', '窓出'),
         False),
        (SFCardViewerRowData('2018/11/25', '', '東武', 'とうきょうスカイツリー', '', '東武', '北千住', '0', '2621', '窓出'),
         False),
        (SFCardViewerRowData('2018/11/25', '', '東武', '北千住', '', '東武', '北千住', '100', '2621', '窓出'),
         False),
        (InstanceResource.ROW_DATA_SF_CARD_VIEWER_EXIT_BY_WINDOW_KITASENJU_STATION, True),
    ])
    def test_is_row_to_skip(
            sf_card_viewer_row_data, expected, yaml_config_load, database_session_stores_sf_card_viewer
    ):
        """Method should return true when entered station is as same as exit station and used amount is 0."""
        sf_card_viewer_row = SFCardViewerEnterExitRow(
            AccountId.PASMO,
            sf_card_viewer_row_data,
            CONFIG.pasmo
        )
        assert sf_card_viewer_row.is_row_to_skip == expected


class TestSFCardViewerRowFactory:
    """Tests for SFCardViewerRowFactory."""
    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        (
            'argument, expected_is_transportation, expected_is_sales_goods, '
            'expected_is_auto_charge, expected_is_exit_by_window, expected_is_bus_tram'
        ),
        [
            (InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION,
             True, False, False, False, False),
            (InstanceResource.ROW_DATA_SF_CARD_VIEWER_SALES_GOODS, False, True, False, False, False),
            (InstanceResource.ROW_DATA_SF_CARD_VIEWER_AUTO_CHARGE_AKIHABARA_STATION, False, False, True, False, False),
            (InstanceResource.ROW_DATA_SF_CARD_VIEWER_EXIT_BY_WINDOW_KITASENJU_STATION,
             False, False, False, True, False),
            (InstanceResource.ROW_DATA_SF_CARD_VIEWER_BUS_TRAM, False, False, False, False, True),
        ]
    )
    def test_create_success(yaml_config_load, database_session_stores_sf_card_viewer, argument: SFCardViewerRowData,
                            expected_is_transportation, expected_is_sales_goods, expected_is_auto_charge,
                            expected_is_exit_by_window, expected_is_bus_tram):
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        sf_card_viewer_row = SFCardViewerRowFactory(lambda: CONFIG.pasmo).create(AccountId.PASMO, argument)
        assert isinstance(sf_card_viewer_row, SFCardViewerRow)
        assert sf_card_viewer_row.is_transportation == expected_is_transportation
        assert sf_card_viewer_row.is_sales_goods == expected_is_sales_goods
        assert sf_card_viewer_row.is_auto_charge == expected_is_auto_charge
        assert sf_card_viewer_row.is_exit_by_window == expected_is_exit_by_window
        assert sf_card_viewer_row.is_bus_tram == expected_is_bus_tram

    @staticmethod
    def test_create_fail(yaml_config_load, database_session_stores_sf_card_viewer):
        """Method should raise ValueError when note is not defined."""
        with pytest.raises(ValueError):
            # pylint: disable=protected-access
            SFCardViewerRowFactory(lambda: CONFIG.pasmo).create(
                AccountId.PASMO, InstanceResource.ROW_DATA_SF_CARD_VIEWER_UNSUPPORTED_NOTE
            )
