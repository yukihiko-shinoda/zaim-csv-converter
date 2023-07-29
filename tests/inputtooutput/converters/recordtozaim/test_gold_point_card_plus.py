"""Tests for gold_point_card_plus.py."""
from dataclasses import dataclass

import pytest

from tests.conftest import create_zaim_row
from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputtooutput.datasources.csv.data.gold_point_card_plus import GoldPointCardPlusRowData
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimPaymentRow, ZaimRow


@pytest.fixture(scope="class")
def zaim_row_converted_by_gold_point_card_plus_zaim_payment_row_converter(
    _yaml_config_load_class_scope: None,
    # Reason: pytest fixture can't use pytest.mark.usefixtures. pylint: disable=unused-argument
    database_session_stores_gold_point_card_plus_class_scope: None,  # noqa: ARG001
    gold_point_card_plus_row_data: GoldPointCardPlusRowData,
) -> ZaimRow:
    return create_zaim_row(Account.GOLD_POINT_CARD_PLUS.value, gold_point_card_plus_row_data)


@pytest.mark.parametrize(
    ("gold_point_card_plus_row_data"),
    [
        (InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC),
        (InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP),
    ],
    scope="class",
)
class TestZaimRowFactory:
    """Tests for GoldPointCardPlusZaimPaymentRowConverter."""

    def test(
        self,
        # Reason: pytest fixture.
        # pylint: disable=unused-argument,redefined-outer-name
        zaim_row_converted_by_gold_point_card_plus_zaim_payment_row_converter: ZaimRow,
    ) -> None:
        assert isinstance(zaim_row_converted_by_gold_point_card_plus_zaim_payment_row_converter, ZaimPaymentRow)


@pytest.fixture(scope="class")
def zaim_row_data_converted_by_gold_point_card_plus_zaim_payment_row_converter(
    # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
    zaim_row_converted_by_gold_point_card_plus_zaim_payment_row_converter: ZaimRow,
) -> ZaimRowData:
    list_zaim_row = zaim_row_converted_by_gold_point_card_plus_zaim_payment_row_converter.convert_to_list()
    return ZaimRowData(*list_zaim_row)


@dataclass
class Expected:
    date: str
    store_name: str
    amount_payment: int
    item_name: str = ""
    cash_flow_source: str = "ヨドバシゴールドポイントカード・プラス"


@pytest.mark.parametrize(
    ("gold_point_card_plus_row_data", "expected"),
    [
        (
            InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC,
            Expected("2018-07-03", "東京電力エナジーパートナー株式会社", 11402),
        ),
        (
            InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP,
            Expected("2018-07-04", "Amazon Japan G.K.", 3456),
        ),
    ],
    scope="class",
)
class TestGoldPointCardPlusZaimPaymentRowConverter:
    """Tests for GoldPointCardPlusZaimPaymentRowConverter."""

    def test_date(
        self,
        # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        zaim_row_data_converted_by_gold_point_card_plus_zaim_payment_row_converter: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_gold_point_card_plus_zaim_payment_row_converter
        assert zaim_row_data.date == expected.date

    def test_store_name(
        self,
        # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        zaim_row_data_converted_by_gold_point_card_plus_zaim_payment_row_converter: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_gold_point_card_plus_zaim_payment_row_converter
        assert zaim_row_data.store_name == expected.store_name

    def test_item_name(
        self,
        # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        zaim_row_data_converted_by_gold_point_card_plus_zaim_payment_row_converter: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_gold_point_card_plus_zaim_payment_row_converter
        assert zaim_row_data.item_name == expected.item_name

    def test_cash_flow_source(
        self,
        # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        zaim_row_data_converted_by_gold_point_card_plus_zaim_payment_row_converter: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_gold_point_card_plus_zaim_payment_row_converter
        assert zaim_row_data.cash_flow_source == expected.cash_flow_source

    def test_amount_payment(
        self,
        # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        zaim_row_data_converted_by_gold_point_card_plus_zaim_payment_row_converter: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_gold_point_card_plus_zaim_payment_row_converter
        assert zaim_row_data.amount_payment == expected.amount_payment
