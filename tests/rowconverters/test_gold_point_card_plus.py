"""Tests for gold_point_card_plus.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRowFactory, GoldPointCardPlusRow
from zaimcsvconverter.models import FileCsvConvertId
from zaimcsvconverter.zaim_row import ZaimPaymentRow, ZaimRowFactory
from zaimcsvconverter.rowconverters.gold_point_card_plus import GoldPointCardPlusZaimPaymentRowConverter, \
    GoldPointCardPlusZaimRowConverterFactory


class TestGoldPointCardPlusZaimPaymentRowConverter:
    """Tests for GoldPointCardPlusZaimPaymentRowConverter."""
    # Reason: Testing different version of row data is better to be separated code.
    # noinspection DuplicatedCode
    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        (
            'gold_point_card_plus_row_data, expected_date, '
            'expected_store_name_zaim, expected_use_amount'
        ),
        [
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC,
                '2018-07-03', '東京電力エナジーパートナー株式会社', 11402
            ),
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP,
                '2018-07-04', 'Amazon Japan G.K.', 3456
            ),
        ]
    )
    def test(
            gold_point_card_plus_row_data,
            expected_date,
            expected_store_name_zaim,
            expected_use_amount,
            yaml_config_load,
            database_session_stores_gold_point_card_plus
    ):
        """Arguments should set into properties."""
        row = GoldPointCardPlusRow(gold_point_card_plus_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(GoldPointCardPlusZaimPaymentRowConverter(row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store_name_zaim
        assert zaim_row_data.item_name == ''
        assert zaim_row_data.cash_flow_source == 'ヨドバシゴールドポイントカード・プラス'
        assert zaim_row_data.amount_payment == expected_use_amount


class TestGoldPointCardPlusZaimRowConverterFactory:
    """Tests for GoldPointCardPlusZaimRowConverterFactory."""
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
        input_row = GoldPointCardPlusRowFactory().create(input_row_data)
        assert isinstance(GoldPointCardPlusZaimRowConverterFactory().create(input_row), expected)
