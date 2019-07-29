"""Tests for sf_card_viewer.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.sf_card_viewer import SFCardViewerRowFactory, SFCardViewerRowData, \
    SFCardViewerRow, SFCardViewerEnterExitRow
from zaimcsvconverter.models import AccountId
from zaimcsvconverter.zaim_row import ZaimTransferRow, ZaimPaymentRow, ZaimRowFactory
from zaimcsvconverter.rowconverters.sf_card_viewer import SFCardViewerZaimRowConverterFactory, \
    SFCardViewerZaimPaymentRowConverter, SFCardViewerZaimTransferRowConverter


class TestSFCardViewerZaimPaymentRowFactory:
    """Tests for SFCardViewerZaimPaymentRowConverter."""
    # pylint: disable=unused-argument
    @staticmethod
    def test(yaml_config_load, database_session_stores_sf_card_viewer):
        """Arguments should set into properties."""
        expected_amount = 195
        config_account_name = 'PASMO'
        sf_card_viewer_row = SFCardViewerEnterExitRow(
            AccountId.PASMO, InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION, CONFIG.pasmo
        )

        class ConcreteSFCardViewerZaimPaymentRowConverter(SFCardViewerZaimPaymentRowConverter):
            # Reason: Raw code is simple enough. pylint: disable=missing-docstring
            account_config = CONFIG.pasmo
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(ConcreteSFCardViewerZaimPaymentRowConverter(sf_card_viewer_row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == '2018-11-13'
        assert zaim_row_data.store_name == '東京地下鉄株式会社　南北線後楽園駅'
        assert zaim_row_data.item_name == ''
        assert zaim_row_data.cash_flow_source == config_account_name
        assert zaim_row_data.note == 'メトロ 六本木一丁目 → メトロ 後楽園'
        assert zaim_row_data.amount_payment == expected_amount


class TestSFCardViewerZaimTransferRowFactory:
    """Tests for SFCardViewerZaimTransferRowConverter."""
    # pylint: disable=unused-argument
    @staticmethod
    def test(yaml_config_load, database_session_stores_sf_card_viewer):
        """Arguments should set into properties."""
        expected_amount = 3000
        config_account_name = 'PASMO'
        config_auto_charge_source = 'TOKYU CARD'
        sf_card_viewer_row = SFCardViewerRow(
            AccountId.PASMO, InstanceResource.ROW_DATA_SF_CARD_VIEWER_AUTO_CHARGE_AKIHABARA_STATION, CONFIG.pasmo
        )

        class ConcreteSFCardViewerZaimTransferRowConverter(SFCardViewerZaimTransferRowConverter):
            # Reason: Raw code is simple enough. pylint: disable=missing-docstring
            account_config = CONFIG.pasmo
        zaim_row = ZaimRowFactory.create(ConcreteSFCardViewerZaimTransferRowConverter(sf_card_viewer_row))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == '2018-11-11'
        assert zaim_row_data.store_name == ''
        assert zaim_row_data.item_name == ''
        assert zaim_row_data.cash_flow_source == config_auto_charge_source
        assert zaim_row_data.cash_flow_target == config_account_name
        assert zaim_row_data.amount_transfer == expected_amount


class TestSFCardViewerZaimRowConverterFactory:
    """Tests for SFCardViewerZaimRowConverterFactory."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'database_session_with_schema, input_row_data, expected',
        [
            # Case when SF Card Viewer transportation
            ([InstanceResource.FIXTURE_RECORD_STORE_PASMO_KOHRAKUEN_STATION],
             InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION,
             SFCardViewerZaimPaymentRowConverter),
            # Case when SF Card Viewer sales goods
            ([InstanceResource.FIXTURE_RECORD_STORE_PASMO_EMPTY],
             InstanceResource.ROW_DATA_SF_CARD_VIEWER_SALES_GOODS, SFCardViewerZaimPaymentRowConverter),
            # Case when SF Card Viewer auto charge
            ([InstanceResource.FIXTURE_RECORD_STORE_PASMO_EMPTY],
             InstanceResource.ROW_DATA_SF_CARD_VIEWER_AUTO_CHARGE_AKIHABARA_STATION,
             SFCardViewerZaimTransferRowConverter),
            # Case when SF Card Viewer exit by window
            ([InstanceResource.FIXTURE_RECORD_STORE_PASMO_KITASENJU_STATION],
             InstanceResource.ROW_DATA_SF_CARD_VIEWER_EXIT_BY_WINDOW_KITASENJU_STATION,
             SFCardViewerZaimPaymentRowConverter),
            # Case when SF Card Viewer bus tram
            ([InstanceResource.FIXTURE_RECORD_STORE_PASMO_EMPTY],
             InstanceResource.ROW_DATA_SF_CARD_VIEWER_BUS_TRAM, SFCardViewerZaimPaymentRowConverter),
        ], indirect=['database_session_with_schema']
    )
    def test_success(yaml_config_load, database_session_with_schema, input_row_data: SFCardViewerRowData, expected):
        """Input row should convert to suitable ZaimRow by transfer target."""
        input_row = SFCardViewerRowFactory(lambda: CONFIG.pasmo).create(AccountId.PASMO, input_row_data)
        factory = SFCardViewerZaimRowConverterFactory(lambda: CONFIG.pasmo).create(input_row)
        # noinspection PyTypeChecker
        assert isinstance(factory, expected)
