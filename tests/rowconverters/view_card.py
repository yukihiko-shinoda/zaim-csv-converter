"""Tests for view_card.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.inputcsvformats.view_card import ViewCardRow, ViewCardRowFactory
from zaimcsvconverter.models import AccountId
from zaimcsvconverter.rowconverters.view_card import ViewCardZaimRowConverterFactory, ViewCardZaimPaymentRowConverter
from zaimcsvconverter.zaim_row import ZaimPaymentRow, ZaimRowFactory


class TestViewCardZaimPaymentRowConverter:
    """Tests for ViewCardZaimPaymentRowConverter."""
    # Reason: Testing different version of row data is better to be separated code.
    # noinspection DuplicatedCode
    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        (
            'view_card_row_data, expected_date, '
            'expected_store_name_zaim, expected_use_amount'
        ),
        [
            (
                InstanceResource.ROW_DATA_VIEW_CARD_ANNUAL_FEE,
                '2020-03-31', 'ビューカード　ビューカードセンター', 524, False
            ),
        ]
    )
    def test(
            view_card_row_data,
            expected_date,
            expected_store_name_zaim,
            expected_use_amount,
            yaml_config_load,
            database_session_stores_view_card
    ):
        """Arguments should set into properties."""
        row = ViewCardRow(AccountId.VIEW_CARD, view_card_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(ViewCardZaimPaymentRowConverter(row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store_name_zaim
        assert zaim_row_data.item_name == ''
        assert zaim_row_data.cash_flow_source == 'ビューカード'
        assert zaim_row_data.amount_payment == expected_use_amount


class TestGoldPointCardPlus201912ZaimRowConverterFactory:
    """Tests for GoldPointCardPlus201912ZaimRowConverterFactory."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'database_session_with_schema, input_row_data, expected',
        [
            # Case when Gold Point Card Plus payment
            ([InstanceResource.FIXTURE_RECORD_STORE_VIEW_CARD_VIEW_CARD],
             InstanceResource.ROW_DATA_VIEW_CARD_ANNUAL_FEE,
             ViewCardZaimPaymentRowConverter),
        ], indirect=['database_session_with_schema']
    )
    def test_select_factory(yaml_config_load, database_session_with_schema, input_row_data, expected):
        """Input row should convert to suitable ZaimRow by transfer target."""
        input_row = ViewCardRowFactory().create(AccountId.VIEW_CARD, input_row_data)
        assert isinstance(ViewCardZaimRowConverterFactory().create(input_row), expected)
