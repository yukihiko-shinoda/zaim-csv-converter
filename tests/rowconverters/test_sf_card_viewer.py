"""Tests for sf_card_viewer.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputcsvformats import InputRow, InputRowData, TypeVarPydantic
from zaimcsvconverter.inputcsvformats.sf_card_viewer import SFCardViewerRowData
from zaimcsvconverter.rowconverters.sf_card_viewer import (
    SFCardViewerZaimPaymentOnSomewhereRowConverter,
    SFCardViewerZaimPaymentOnStationRowConverter,
    SFCardViewerZaimTransferRowConverter,
)
from zaimcsvconverter.rowconverters import ZaimRowConverter
from zaimcsvconverter.zaim.zaim_row import ZaimPaymentRow, ZaimRowFactory, ZaimTransferRow


class TestSFCardViewerZaimPaymentOnStationRowConverter:
    """Tests for SFCardViewerZaimPaymentOnStationRowConverter."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_sf_card_viewer")
    def test() -> None:
        """Arguments should set into properties."""
        expected_amount = 195
        config_account_name = "PASMO"
        account_context = Account.PASMO.value
        sf_card_viewer_row = account_context.create_input_row_instance(
            InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION
        )
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(sf_card_viewer_row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == "2018-11-13"
        assert zaim_row_data.store_name == "東京地下鉄株式会社　南北線後楽園駅"
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_source == config_account_name
        assert zaim_row_data.note == "メトロ 六本木一丁目 → メトロ 後楽園"
        assert zaim_row_data.amount_payment == expected_amount


class TestSFCardViewerZaimTransferRowConverter:
    """Tests for SFCardViewerZaimTransferRowConverter."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_sf_card_viewer")
    def test() -> None:
        """Arguments should set into properties."""
        expected_amount = 3000
        config_account_name = "PASMO"
        config_auto_charge_source = "TOKYU CARD"
        account_context = Account.PASMO.value
        sf_card_viewer_row = account_context.create_input_row_instance(
            InstanceResource.ROW_DATA_SF_CARD_VIEWER_AUTO_CHARGE_AKIHABARA_STATION
        )
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(sf_card_viewer_row))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == "2018-11-11"
        assert zaim_row_data.store_name == ""
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_source == config_auto_charge_source
        assert zaim_row_data.cash_flow_target == config_account_name
        assert zaim_row_data.amount_transfer == expected_amount


class TestSFCardViewerZaimRowConverterFactory:
    """Tests for SFCardViewerZaimRowConverterFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema, input_row_data, expected",
        [
            # Case when SF Card Viewer transportation
            (
                [InstanceResource.FIXTURE_RECORD_STORE_PASMO_KOHRAKUEN_STATION],
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION,
                SFCardViewerZaimPaymentOnStationRowConverter,
            ),
            # Case when SF Card Viewer sales goods
            (
                [InstanceResource.FIXTURE_RECORD_STORE_PASMO_EMPTY],
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_SALES_GOODS,
                SFCardViewerZaimPaymentOnSomewhereRowConverter,
            ),
            # Case when SF Card Viewer auto charge
            (
                [InstanceResource.FIXTURE_RECORD_STORE_PASMO_EMPTY],
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_AUTO_CHARGE_AKIHABARA_STATION,
                SFCardViewerZaimTransferRowConverter,
            ),
            # Case when SF Card Viewer exit by window
            (
                [InstanceResource.FIXTURE_RECORD_STORE_PASMO_KITASENJU_STATION],
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_EXIT_BY_WINDOW_KITASENJU_STATION,
                SFCardViewerZaimPaymentOnStationRowConverter,
            ),
            # Case when SF Card Viewer bus tram
            (
                [InstanceResource.FIXTURE_RECORD_STORE_PASMO_EMPTY],
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_BUS_TRAM,
                SFCardViewerZaimPaymentOnSomewhereRowConverter,
            ),
        ],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test_success(
        input_row_data: SFCardViewerRowData,
        expected: type[ZaimRowConverter[InputRow[InputRowData[TypeVarPydantic]], InputRowData[TypeVarPydantic]]],
    ) -> None:
        """Input row should convert to suitable ZaimRow by transfer target."""
        account_context = Account.PASMO.value
        sf_card_viewer_row = account_context.create_input_row_instance(input_row_data)
        factory = account_context.zaim_row_converter_factory.create(sf_card_viewer_row)
        # noinspection PyTypeChecker
        assert isinstance(factory, expected)
