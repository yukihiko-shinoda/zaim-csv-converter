"""Tests for GoldPointCartPlusRow."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRow, GoldPointCardPlusRowData, \
    GoldPointCardPlusRowFactory
from zaimcsvconverter.models import Store, AccountId


class TestGoldPointCardPlusRowData:
    """Tests for GoldPointCardPlusRowData."""
    @staticmethod
    # pylint: disable=too-many-locals
    def test_init_and_property():
        """
        Property date should return datetime object.
        Property store_date should return used_store.
        """
        used_date = '2018/7/3'
        used_store = '東京電力  電気料金等'
        used_card = 'ご本人'
        payment_kind = '1回払い'
        number_of_division = ''
        scheduled_payment_month = '18/8'
        used_amount = '11402'
        unknown_1 = '11402'
        unknown_2 = 'unknown 2'
        unknown_3 = 'unknown 3'
        unknown_4 = 'unknown 4'
        unknown_6 = 'unknown 5'
        unknown_5 = 'unknown 6'
        gold_point_card_plus_row_data = GoldPointCardPlusRowData(used_date, used_store, used_card, payment_kind,
                                                                 number_of_division, scheduled_payment_month,
                                                                 used_amount, unknown_1, unknown_2, unknown_3,
                                                                 unknown_4, unknown_5, unknown_6)
        assert gold_point_card_plus_row_data.used_card == used_card
        assert gold_point_card_plus_row_data.payment_kind == payment_kind
        assert gold_point_card_plus_row_data.number_of_division == number_of_division
        assert gold_point_card_plus_row_data.scheduled_payment_month == scheduled_payment_month
        assert gold_point_card_plus_row_data.used_amount == used_amount
        assert gold_point_card_plus_row_data.unknown_1 == unknown_1
        assert gold_point_card_plus_row_data.unknown_2 == unknown_2
        assert gold_point_card_plus_row_data.unknown_3 == unknown_3
        assert gold_point_card_plus_row_data.unknown_4 == unknown_4
        assert gold_point_card_plus_row_data.unknown_5 == unknown_5
        assert gold_point_card_plus_row_data.unknown_6 == unknown_6
        assert gold_point_card_plus_row_data.date == datetime(2018, 7, 3, 0, 0)
        assert gold_point_card_plus_row_data.store_name == used_store


class TestGoldPointCardPlusRow:
    """Tests for GoldPointCartPlusRow."""
    # pylint: disable=protected-access,too-many-arguments,unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        (
            'gold_point_card_plus_row_data, expected_date, expected_store_name_zaim, expected_is_row_to_skip'
        ),
        [
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC,
                datetime(2018, 7, 3, 0, 0, 0), '東京電力エナジーパートナー株式会社', False
            ),
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP,
                datetime(2018, 7, 4, 0, 0, 0), 'Amazon Japan G.K.', True
            ),
        ]
    )
    def test_init(
            yaml_config_load,
            database_session_stores_gold_point_card_plus,
            gold_point_card_plus_row_data,
            expected_date,
            expected_store_name_zaim,
            expected_is_row_to_skip
    ):
        """
        Arguments should set into properties.
        :param GoldPointCardPlusRowData gold_point_card_plus_row_data:
        """
        row = GoldPointCardPlusRow(AccountId.GOLD_POINT_CARD_PLUS, gold_point_card_plus_row_data)
        validated_row = row.validate()
        assert row.zaim_date == expected_date
        assert isinstance(row.store, Store)
        # pylint: disable=protected-access
        assert row.store.name == gold_point_card_plus_row_data._used_store
        assert row.store.name_zaim == expected_store_name_zaim
        assert row.is_row_to_skip(validated_row.store) == expected_is_row_to_skip


class TestGoldPointCardPlusRowFactory:
    """Tests for GoldPointCardPlusRowFactory."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize('argument, expected', [
        (InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC, GoldPointCardPlusRow),
    ])
    def test_create(argument, expected, database_session_stores_gold_point_card_plus):
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        gold_point_card_plus_row = GoldPointCardPlusRowFactory().create(AccountId.MUFG, argument)
        assert isinstance(gold_point_card_plus_row, expected)
