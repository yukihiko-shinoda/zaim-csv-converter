"""Tests for view_card.py."""

import pytest

from tests.conftest import create_zaim_row
from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.accounts.enum import Account
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.view_card import ViewCardRowData
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimPaymentRow
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimRow


@pytest.fixture(scope="class")
def zaim_row_converted_by_view_card_zaim_payment_row_converter(
    _yaml_config_load_class_scope: None,
    # Reason: pytest fixture can't use pytest.mark.usefixtures. pylint: disable=unused-argument
    database_session_stores_view_card_class_scope: None,  # noqa: ARG001
    view_card_row_data: ViewCardRowData,
) -> ZaimRow:
    return create_zaim_row(Account.VIEW_CARD.value, view_card_row_data)


@pytest.mark.parametrize("view_card_row_data", [InstanceResource.ROW_DATA_VIEW_CARD_ANNUAL_FEE], scope="class")
class TestZaimRowFactory:
    # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
    def test(self, zaim_row_converted_by_view_card_zaim_payment_row_converter: ZaimRow) -> None:
        assert isinstance(zaim_row_converted_by_view_card_zaim_payment_row_converter, ZaimPaymentRow)


@pytest.fixture(scope="class")
def zaim_row_data_converted_by_view_card_zaim_payment_row_converter(
    # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
    zaim_row_converted_by_view_card_zaim_payment_row_converter: ZaimRow,
) -> ZaimRowData:
    list_zaim_row = zaim_row_converted_by_view_card_zaim_payment_row_converter.convert_to_list()
    return ZaimRowData(*list_zaim_row)


@pytest.mark.parametrize(
    "view_card_row_data",
    [InstanceResource.ROW_DATA_VIEW_CARD_ANNUAL_FEE],
    scope="class",
)
class TestViewCardZaimPaymentRowConverter:
    """Tests for ViewCardZaimPaymentRowConverter."""

    # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
    def test_date(self, zaim_row_data_converted_by_view_card_zaim_payment_row_converter: ZaimRowData) -> None:
        """Arguments should set into properties."""
        assert zaim_row_data_converted_by_view_card_zaim_payment_row_converter.date == "2020-03-31"

    def test_store_name(self, zaim_row_data_converted_by_view_card_zaim_payment_row_converter: ZaimRowData) -> None:
        """Arguments should set into properties."""
        store_name = "ビューカード　ビューカードセンター"
        assert zaim_row_data_converted_by_view_card_zaim_payment_row_converter.store_name == store_name

    def test_item_name(self, zaim_row_data_converted_by_view_card_zaim_payment_row_converter: ZaimRowData) -> None:
        """Arguments should set into properties."""
        assert not zaim_row_data_converted_by_view_card_zaim_payment_row_converter.item_name

    def test_cash_flow_source(
        self,
        zaim_row_data_converted_by_view_card_zaim_payment_row_converter: ZaimRowData,
    ) -> None:
        """Arguments should set into properties."""
        assert zaim_row_data_converted_by_view_card_zaim_payment_row_converter.cash_flow_source == "ビューカード"

    def test_amount_payment(
        self,
        zaim_row_data_converted_by_view_card_zaim_payment_row_converter: ZaimRowData,
    ) -> None:
        """Arguments should set into properties."""
        expected_use_amount = 524
        assert zaim_row_data_converted_by_view_card_zaim_payment_row_converter.amount_payment == expected_use_amount
