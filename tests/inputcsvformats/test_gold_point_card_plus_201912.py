"""Tests for GoldPointCartPlusRow."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputcsvformats.gold_point_card_plus_201912 import GoldPointCardPlus201912RowData, \
    GoldPointCardPlus201912Row, GoldPointCardPlus201912RowFactory
from zaimcsvconverter.models import Store, FileCsvConvertId


class TestGoldPointCardPlus201912RowData:
    """Tests for GoldPointCardPlusRowData."""
    # Reason: asserting properties can't be short no more.
    # noinspection DuplicatedCode
    @staticmethod
    # pylint: disable=too-many-locals
    def test_init_and_property():
        """
        Property date should return datetime object.
        Property store_date should return used_store.
        """
        used_date = '2019/11/03'
        used_store = 'AMAZON WEB SERVICES (AWS.AMAZON.CO)'
        used_amount = '66'
        number_of_division = '1'
        current_time_of_division = '1'
        payed_amount = '66'
        others = '0.60　USD　110.712　11 03'
        gold_point_card_plus_row_data = GoldPointCardPlus201912RowData(
            used_date, used_store, used_amount, number_of_division, current_time_of_division, payed_amount, others)
        assert gold_point_card_plus_row_data.date == datetime(2019, 11, 3, 0, 0)
        assert gold_point_card_plus_row_data.store_name == used_store
        assert gold_point_card_plus_row_data.payed_amount == 66


class TestGoldPointCardPlus201912Row:
    """Tests for GoldPointCartPlusRow."""
    # pylint: disable=protected-access,too-many-arguments,unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        (
            'gold_point_card_plus_201912_row_data, expected_date, expected_store_name_zaim, expected_is_row_to_skip'
        ),
        [
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_TOKYO_ELECTRIC,
                datetime(2019, 11, 5, 0, 0, 0), '東京電力エナジーパートナー株式会社', False
            ),
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_AMAZON_DOWNLOADS,
                datetime(2019, 11, 9, 0, 0, 0), 'Amazon Japan G.K.', True
            ),
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_AWS,
                datetime(2019, 11, 3, 0, 0, 0), 'Amazon Web Services Japan K.K.', False
            ),
        ]
    )
    def test_init(
            yaml_config_load,
            database_session_stores_gold_point_card_plus,
            gold_point_card_plus_201912_row_data,
            expected_date,
            expected_store_name_zaim,
            expected_is_row_to_skip
    ):
        """
        Arguments should set into properties.
        :param GoldPointCardPlus201912RowData gold_point_card_plus_201912_row_data:
        """
        row = GoldPointCardPlus201912Row(gold_point_card_plus_201912_row_data)
        assert row.date == expected_date
        assert isinstance(row.store, Store)
        # pylint: disable=protected-access
        assert row.store.name == gold_point_card_plus_201912_row_data._used_store
        assert row.store.name_zaim == expected_store_name_zaim
        assert row.is_row_to_skip == expected_is_row_to_skip

    @staticmethod
    def test_is_row_to_skip(database_session_stores_gold_point_card_plus):
        assert GoldPointCardPlus201912Row(
            InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_YAHOO_JAPAN
        ).is_row_to_skip is False


class TestGoldPointCardPlus201912RowFactory:
    """Tests for GoldPointCardPlusRowFactory."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize('argument, expected', [
        (InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_TOKYO_ELECTRIC, GoldPointCardPlus201912Row),
    ])
    def test_create(argument, expected, database_session_stores_gold_point_card_plus):
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        gold_point_card_plus_row = GoldPointCardPlus201912RowFactory().create(argument)
        assert isinstance(gold_point_card_plus_row, expected)
