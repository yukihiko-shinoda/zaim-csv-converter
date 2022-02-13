"""Tests for gold_point_card_plus_201912.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputcsvformats.gold_point_card_plus_201912 import GoldPointCardPlus201912RowData
from zaimcsvconverter.rowconverters.gold_point_card_plus_201912 import GoldPointCardPlus201912ZaimPaymentRowConverter
from zaimcsvconverter.zaim_row import ZaimPaymentRow, ZaimRowFactory


class TestGoldPointCardPlus201912ZaimPaymentRowConverter:
    """Tests for GoldPointCardPlus201912ZaimPaymentRowConverter."""

    # Reason: Testing different version of row data is better to be separated code.
    # noinspection DuplicatedCode
    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        "gold_point_card_plus_201912_row_data, expected_date, expected_store_name_zaim, expected_use_amount",
        [
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_TOKYO_ELECTRIC,
                "2019-11-05",
                "東京電力エナジーパートナー株式会社",
                11905,
            ),
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_AMAZON_DOWNLOADS,
                "2019-11-09",
                "Amazon Japan G.K.",
                1969,
            ),
        ],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_gold_point_card_plus")
    def test(
        gold_point_card_plus_201912_row_data: GoldPointCardPlus201912RowData,
        expected_date: str,
        expected_store_name_zaim: str,
        expected_use_amount: int,
    ) -> None:
        """Arguments should set into properties."""
        accout_context = Account.GOLD_POINT_CARD_PLUS_201912.value
        row = accout_context.create_input_row_instance(gold_point_card_plus_201912_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(accout_context.zaim_row_converter_factory.create(row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store_name_zaim
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_source == "ヨドバシゴールドポイントカード・プラス"
        assert zaim_row_data.amount_payment == expected_use_amount


class TestGoldPointCardPlus201912ZaimRowConverterFactory:
    """Tests for GoldPointCardPlus201912ZaimRowConverterFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema, input_row_data, expected",
        [
            # Case when Gold Point Card Plus payment
            (
                [InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP],
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_AMAZON_DOWNLOADS,
                GoldPointCardPlus201912ZaimPaymentRowConverter,
            ),
        ],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test_select_factory(
        input_row_data: GoldPointCardPlus201912RowData, expected: type[GoldPointCardPlus201912ZaimPaymentRowConverter]
    ) -> None:
        """Input row should convert to suitable ZaimRow by transfer target."""
        accout_context = Account.GOLD_POINT_CARD_PLUS_201912.value
        input_row = accout_context.create_input_row_instance(input_row_data)
        actual = accout_context.zaim_row_converter_factory.create(input_row)
        assert isinstance(actual, expected)
