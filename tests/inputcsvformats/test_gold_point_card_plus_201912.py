"""Tests for GoldPointCartPlusRow."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputcsvformats.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912Row,
    GoldPointCardPlus201912RowData,
    GoldPointCardPlus201912RowFactory,
)
from zaimcsvconverter.inputcsvformats import RowDataFactory
from zaimcsvconverter.models import Store


class TestGoldPointCardPlus201912RowData:
    """Tests for GoldPointCardPlusRowData."""

    # Reason: asserting properties can't be short no more.
    # noinspection DuplicatedCode
    @staticmethod
    # pylint: disable=too-many-locals
    def test_init_and_property() -> None:
        """Tests following:

        - Property date should return datetime object.
        - Property store_date should return used_store.
        """
        used_date = "2019/11/03"
        used_store = "AMAZON WEB SERVICES (AWS.AMAZON.CO)"
        used_amount = "66"
        number_of_division = "1"
        current_time_of_division = "1"
        payed_amount = "66"
        others = "0.60　USD　110.712　11 03"
        gold_point_card_plus_row_data = RowDataFactory(GoldPointCardPlus201912RowData).create(
            [used_date, used_store, used_amount, number_of_division, current_time_of_division, payed_amount, others]
        )
        assert gold_point_card_plus_row_data.date == datetime(2019, 11, 3, 0, 0)
        assert gold_point_card_plus_row_data.store_name == used_store
        assert gold_point_card_plus_row_data.payed_amount == 66


class TestGoldPointCardPlus201912Row:
    """Tests for GoldPointCartPlusRow."""

    # pylint: disable=protected-access,too-many-arguments,unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "gold_point_card_plus_201912_row_data, expected_date, expected_store_name_zaim, expected_is_row_to_skip",
        [
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_TOKYO_ELECTRIC,
                datetime(2019, 11, 5, 0, 0, 0),
                "東京電力エナジーパートナー株式会社",
                False,
            ),
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_AMAZON_DOWNLOADS,
                datetime(2019, 11, 9, 0, 0, 0),
                "Amazon Japan G.K.",
                True,
            ),
            # Since アマゾン注文履歴フィルタ doesn't suppport return
            # see: https://github.com/furyutei/amzOrderHistoryFilter/blob/30ff80c6ea5194ec4b9ede986e30b80cbdd21355/src/js/amzOrderHistoryFilter.user.js#L4157 # noqa E501 pylint: disable=line-too-long
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_AMAZON_RETURN,
                datetime(2020, 12, 18, 0, 0, 0),
                "Amazon Japan G.K.",
                False,
            ),
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_AWS,
                datetime(2019, 11, 3, 0, 0, 0),
                "Amazon Web Services Japan K.K.",
                False,
            ),
        ],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_gold_point_card_plus")
    def test_init(
        gold_point_card_plus_201912_row_data: GoldPointCardPlus201912RowData,
        expected_date: datetime,
        expected_store_name_zaim: str,
        expected_is_row_to_skip: bool,
    ) -> None:
        """Arguments should set into properties.

        :param GoldPointCardPlus201912RowData gold_point_card_plus_201912_row_data:
        """
        row = GoldPointCardPlus201912Row(gold_point_card_plus_201912_row_data)
        assert row.date == expected_date
        assert isinstance(row.store, Store)
        # pylint: disable=protected-access
        assert row.store.name == gold_point_card_plus_201912_row_data.used_store
        assert row.store.name_zaim == expected_store_name_zaim
        assert row.is_row_to_skip == expected_is_row_to_skip

    @staticmethod
    @pytest.mark.usefixtures("database_session_stores_gold_point_card_plus")
    def test_is_row_to_skip() -> None:
        assert (
            GoldPointCardPlus201912Row(
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_YAHOO_JAPAN
            ).is_row_to_skip
            is False
        )


class TestGoldPointCardPlus201912RowFactory:
    """Tests for GoldPointCardPlusRowFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "argument, expected",
        [(InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_TOKYO_ELECTRIC, GoldPointCardPlus201912Row)],
    )
    @pytest.mark.usefixtures("database_session_stores_gold_point_card_plus")
    def test_create(argument: GoldPointCardPlus201912RowData, expected: type[GoldPointCardPlus201912Row]) -> None:
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        gold_point_card_plus_row = GoldPointCardPlus201912RowFactory().create(argument)
        assert isinstance(gold_point_card_plus_row, expected)
