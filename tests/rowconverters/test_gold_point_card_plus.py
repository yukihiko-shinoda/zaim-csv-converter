"""Tests for gold_point_card_plus.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.zaim_row_data import ZaimRowData
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRowFactory, GoldPointCardPlusRow
from zaimcsvconverter.models import AccountId
from zaimcsvconverter.zaim_row import ZaimPaymentRow
from zaimcsvconverter.rowconverters.gold_point_card_plus import GoldPointCardPlusZaimPaymentRowConverter, \
    GoldPointCardPlusZaimRowConverterSelector


class TestGoldPointCardPlusZaimPaymentRowConverter:
    """Tests for GoldPointCardPlusZaimPaymentRowConverter."""
    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        (
            'gold_point_card_plus_row_data, expected_date, '
            'expected_store_name_zaim, expected_use_amount, expected_is_row_to_skip'
        ),
        [
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC,
                '2018-07-03', '東京電力エナジーパートナー株式会社', 11402, False
            ),
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP,
                '2018-07-04', 'Amazon Japan G.K.', 3456, True
            ),
        ]
    )
    def test(
            gold_point_card_plus_row_data,
            expected_date,
            expected_store_name_zaim,
            expected_use_amount,
            expected_is_row_to_skip,
            yaml_config_load,
            database_session_stores_gold_point_card_plus
    ):
        """Arguments should set into properties."""
        row = GoldPointCardPlusRow(AccountId.GOLD_POINT_CARD_PLUS, gold_point_card_plus_row_data)
        validated_input_row = row.validate()
        zaim_row = GoldPointCardPlusZaimPaymentRowConverter(validated_input_row).convert()
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store_name_zaim
        assert zaim_row_data.item_name is None
        assert zaim_row_data.cash_flow_source == 'ヨドバシゴールドポイントカード・プラス'
        assert zaim_row_data.amount_payment == expected_use_amount


class TestGoldPointCardPlusZaimRowConverterSelector:
    """Tests for GoldPointCardPlusZaimRowConverterSelector."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'database_session_with_schema, input_row_data, expected',
        [
            # Case when Gold Point Card Plus payment
            ([InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP],
             InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP, GoldPointCardPlusZaimPaymentRowConverter),
        ], indirect=['database_session_with_schema']
    )
    def test_select_factory(yaml_config_load, database_session_with_schema, input_row_data, expected):
        """Input row should convert to suitable ZaimRow by transfer target."""
        validated_input_row = GoldPointCardPlusRowFactory().create(
            AccountId.GOLD_POINT_CARD_PLUS, input_row_data
        ).validate()
        assert GoldPointCardPlusZaimRowConverterSelector().select(validated_input_row) == expected
