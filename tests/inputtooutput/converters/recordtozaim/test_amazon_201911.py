"""Tests for amazon.py."""

import pytest

from tests.conftest import create_zaim_row
from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.amazon_201911 import Amazon201911RowData
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimPaymentRow
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimRow


@pytest.fixture(scope="class")
def zaim_row_converted_by_amazon_201911_zaim_payment_row_converter(
    _yaml_config_load_class_scope: None,
    # Reason: pytest fixture can't use pytest.mark.usefixtures. pylint: disable=unused-argument
    database_session_item_class_scope: None,  # noqa: ARG001
    amazon_201911_row_data: Amazon201911RowData,
) -> ZaimRow:
    return create_zaim_row(Account.AMAZON_201911.value, amazon_201911_row_data)


@pytest.mark.parametrize(
    "amazon_201911_row_data",
    [InstanceResource.ROW_DATA_AMAZON_201911_AMAZON_POINT, InstanceResource.ROW_DATA_AMAZON_201911_ECHO_DOT],
    scope="class",
)
class TestZaimRowFactory:
    # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
    def test(self, zaim_row_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRow) -> None:
        assert isinstance(zaim_row_converted_by_amazon_201911_zaim_payment_row_converter, ZaimPaymentRow)


@pytest.fixture(scope="class")
def zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter(
    # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
    zaim_row_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRow,
) -> ZaimRowData:
    list_zaim_row = zaim_row_converted_by_amazon_201911_zaim_payment_row_converter.convert_to_list()
    return ZaimRowData(*list_zaim_row)


@pytest.mark.parametrize(
    "amazon_201911_row_data",
    [InstanceResource.ROW_DATA_AMAZON_201911_AMAZON_POINT],
    scope="class",
)
class TestAmazon201911DiscountZaimPaymentRowConverter:
    """Tests for Amazon201911ZaimPaymentRowConverter."""

    def test_date(
        self,
        # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRowData,
    ) -> None:
        """Arguments should set into properties."""
        assert zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter.date == "2019-11-09"

    def test_store_name(
        self,
        # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRowData,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter
        assert zaim_row_data.store_name == "Amazon Japan G.K."

    def test_item_name(
        self,
        # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRowData,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter
        assert zaim_row_data.item_name == "（Amazon ポイント）"  # noqa: RUF001

    def test_cash_flow_source(
        self,
        # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRowData,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter
        assert zaim_row_data.cash_flow_source == "ヨドバシゴールドポイントカード・プラス"

    def test_note(
        self,
        # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRowData,
    ) -> None:
        """Arguments should set into properties."""
        assert not zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter.note

    def test_amount_payment(
        self,
        # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRowData,
    ) -> None:
        """Arguments should set into properties."""
        expected_amount = -11
        zaim_row_data = zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter
        assert zaim_row_data.amount_payment == expected_amount


@pytest.mark.parametrize(
    "amazon_201911_row_data",
    [InstanceResource.ROW_DATA_AMAZON_201911_ECHO_DOT],
    scope="class",
)
class TestAmazon201911PaymentZaimPaymentRowConverter:
    """Tests for Amazon201911ZaimPaymentRowConverter."""

    # Reason: pytest fixture. pylint: disable=unused-argument,redefined-outer-name
    def test_date(self, zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRowData) -> None:
        """Arguments should set into properties."""
        assert zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter.date == "2019-11-09"

    def test_store_name(
        self,
        zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRowData,
    ) -> None:
        """Arguments should set into properties."""
        assert zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter.store_name == "Amazon Japan G.K."

    def test_item_name(self, zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRowData) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter
        assert zaim_row_data.item_name == "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト"

    def test_cash_flow_source(
        self,
        zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRowData,
    ) -> None:
        """Arguments should set into properties."""
        zaim_row_data = zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter
        assert zaim_row_data.cash_flow_source == "ヨドバシゴールドポイントカード・プラス"

    def test_note(self, zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRowData) -> None:
        """Arguments should set into properties."""
        assert not zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter.note

    def test_amount_payment(
        self,
        zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter: ZaimRowData,
    ) -> None:
        """Arguments should set into properties."""
        expected_amount = 4980
        assert zaim_row_data_converted_by_amazon_201911_zaim_payment_row_converter.amount_payment == expected_amount
