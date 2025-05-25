"""Tests for sf_card_viewer.py."""

from dataclasses import dataclass

import pytest

from tests.conftest import create_zaim_row
from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.accounts.enum import Account
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.sf_card_viewer import SFCardViewerRowData
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimPaymentRow
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimRow
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimTransferRow


@pytest.fixture(scope="class")
def zaim_row_converted_by_sf_card_viewer_zaim_payment_row_converter(
    _yaml_config_load_class_scope: None,
    # Reason: pytest fixture can't use pytest.mark.usefixtures. pylint: disable=unused-argument
    database_session_stores_sf_card_viewer_class_scope: None,  # noqa: ARG001
    sf_card_viewer_row_data: SFCardViewerRowData,
) -> ZaimRow:
    return create_zaim_row(Account.PASMO.value, sf_card_viewer_row_data)


@pytest.mark.parametrize(
    ("sf_card_viewer_row_data", "expected"),
    [
        (InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION, ZaimPaymentRow),
        (InstanceResource.ROW_DATA_SF_CARD_VIEWER_AUTO_CHARGE_AKIHABARA_STATION, ZaimTransferRow),
    ],
    scope="class",
)
class TestZaimRowFactory:
    def test(
        self,
        # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        zaim_row_converted_by_sf_card_viewer_zaim_payment_row_converter: ZaimRow,
        expected: type[ZaimRow],
    ) -> None:
        assert isinstance(zaim_row_converted_by_sf_card_viewer_zaim_payment_row_converter, expected)


@pytest.fixture(scope="class")
def zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter(
    # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
    zaim_row_converted_by_sf_card_viewer_zaim_payment_row_converter: ZaimRow,
) -> ZaimRowData:
    list_zaim_row = zaim_row_converted_by_sf_card_viewer_zaim_payment_row_converter.convert_to_list()
    return ZaimRowData(*list_zaim_row)


@dataclass
class Expected:
    date: str
    store_name: str
    item_name: str
    cash_flow_source: str
    cash_flow_target: str
    amount_payment: int
    amount_transfer: int
    note: str


@pytest.mark.parametrize(
    ("sf_card_viewer_row_data", "expected"),
    [
        (
            InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION,
            Expected(
                "2018-11-13",
                "東京地下鉄株式会社　南北線後楽園駅",
                "",
                "PASMO",
                "",
                195,
                0,
                "メトロ 六本木一丁目 → メトロ 後楽園",
            ),
        ),
        (
            InstanceResource.ROW_DATA_SF_CARD_VIEWER_AUTO_CHARGE_AKIHABARA_STATION,
            Expected(
                "2018-11-11",
                "",
                "",
                "TOKYU CARD",
                "PASMO",
                0,
                3000,
                "",
            ),
        ),
    ],
    scope="class",
)
class TestSFCardViewerZaimPaymentOnStationRowConverter:
    """Tests for SFCardViewerZaimPaymentOnStationRowConverter."""

    # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
    def test_date(
        self,
        zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter
        assert zaim_row_data.date == expected.date

    def test_store_name(
        self,
        zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter
        assert zaim_row_data.store_name == expected.store_name

    def test_item_name(
        self,
        zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Arguments should set into properties."""
        assert zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter.item_name == expected.item_name

    def test_cash_flow_source(
        self,
        zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter
        assert zaim_row_data.cash_flow_source == expected.cash_flow_source

    def test_note(
        self,
        zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter
        assert zaim_row_data.note == expected.note

    def test_amount_payment(
        self,
        zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_sf_card_viewer_zaim_payment_row_converter
        assert zaim_row_data.amount_payment == expected.amount_payment
