"""Tests for gold_point_card_plus_201912.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.inputcsvformats.gold_point_card_plus_201912 import GoldPointCardPlus201912Row, \
    GoldPointCardPlus201912RowFactory
from zaimcsvconverter.models import AccountId
from zaimcsvconverter.rowconverters.gold_point_card_plus_201912 import GoldPointCardPlus201912ZaimPaymentRowConverter, \
    GoldPointCardPlus201912ZaimRowConverterFactory
from zaimcsvconverter.zaim_row import ZaimPaymentRow, ZaimRowFactory


class TestGoldPointCardPlus201912ZaimPaymentRowConverter:
    """Tests for GoldPointCardPlus201912ZaimPaymentRowConverter."""
    # Reason: Testing different version of row data is better to be separated code.
    # noinspection DuplicatedCode
    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        (
            'gold_point_card_plus_201912_row_data, expected_date, '
            'expected_store_name_zaim, expected_use_amount, expected_is_row_to_skip'
        ),
        [
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_TOKYO_ELECTRIC,
                '2019-11-05', '東京電力エナジーパートナー株式会社', 11905, False
            ),
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_AMAZON_DOWNLOADS,
                '2019-11-09', 'Amazon Japan G.K.', 1969, True
            ),
        ]
    )
    def test(
            gold_point_card_plus_201912_row_data,
            expected_date,
            expected_store_name_zaim,
            expected_use_amount,
            expected_is_row_to_skip,
            yaml_config_load,
            database_session_stores_gold_point_card_plus
    ):
        """Arguments should set into properties."""
        row = GoldPointCardPlus201912Row(AccountId.GOLD_POINT_CARD_PLUS, gold_point_card_plus_201912_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(GoldPointCardPlus201912ZaimPaymentRowConverter(row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store_name_zaim
        assert zaim_row_data.item_name == ''
        assert zaim_row_data.cash_flow_source == 'ヨドバシゴールドポイントカード・プラス'
        assert zaim_row_data.amount_payment == expected_use_amount


class TestGoldPointCardPlus201912ZaimRowConverterFactory:
    """Tests for GoldPointCardPlus201912ZaimRowConverterFactory."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'database_session_with_schema, input_row_data, expected',
        [
            # Case when Gold Point Card Plus payment
            ([InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP],
             InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_AMAZON_DOWNLOADS,
             GoldPointCardPlus201912ZaimPaymentRowConverter),
        ], indirect=['database_session_with_schema']
    )
    def test_select_factory(yaml_config_load, database_session_with_schema, input_row_data, expected):
        """Input row should convert to suitable ZaimRow by transfer target."""
        input_row = GoldPointCardPlus201912RowFactory().create(AccountId.GOLD_POINT_CARD_PLUS, input_row_data)
        assert isinstance(GoldPointCardPlus201912ZaimRowConverterFactory().create(input_row), expected)
