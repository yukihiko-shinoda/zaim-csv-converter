"""Tests for view_card.py."""
from pathlib import Path

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputtooutput.converters.recordtozaim.view_card import ViewCardZaimPaymentRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputtooutput.datasources.csv.data.view_card import ViewCardRowData
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimPaymentRow


class TestViewCardZaimPaymentRowConverter:
    """Tests for ViewCardZaimPaymentRowConverter."""

    # Reason: Testing different version of row data is better to be separated code.
    # noinspection DuplicatedCode
    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        ("view_card_row_data", "expected_date", "expected_store_name_zaim", "expected_use_amount"),
        [(InstanceResource.ROW_DATA_VIEW_CARD_ANNUAL_FEE, "2020-03-31", "ビューカード　ビューカードセンター", 524)],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_view_card")
    def test(
        view_card_row_data: ViewCardRowData,
        expected_date: str,
        expected_store_name_zaim: str,
        expected_use_amount: int,
    ) -> None:
        """Arguments should set into properties."""
        account_context = Account.VIEW_CARD.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        row = csv_record_processor.create_input_row_instance(view_card_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(row, Path()))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store_name_zaim
        assert not zaim_row_data.item_name
        assert zaim_row_data.cash_flow_source == "ビューカード"
        assert zaim_row_data.amount_payment == expected_use_amount


class TestGoldPointCardPlus201912ZaimRowConverterFactory:
    """Tests for GoldPointCardPlus201912ZaimRowConverterFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        ("database_session_with_schema", "input_row_data", "expected"),
        [
            # Case when Gold Point Card Plus payment
            (
                [InstanceResource.FIXTURE_RECORD_STORE_VIEW_CARD_VIEW_CARD],
                InstanceResource.ROW_DATA_VIEW_CARD_ANNUAL_FEE,
                ViewCardZaimPaymentRowConverter,
            ),
        ],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_with_schema")
    def test_select_factory(input_row_data: ViewCardRowData, expected: type[ViewCardZaimPaymentRowConverter]) -> None:
        """Input row should convert to suitable ZaimRow by transfer target."""
        account_context = Account.VIEW_CARD.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        input_row = csv_record_processor.create_input_row_instance(input_row_data)
        actual = account_context.zaim_row_converter_factory.create(input_row, Path())
        assert isinstance(actual, expected)
