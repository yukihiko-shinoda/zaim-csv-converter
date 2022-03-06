"""Tests for GoldPointCartPlusRow."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.data.gold_point_card_plus import GoldPointCardPlusRowData
from zaimcsvconverter.inputtooutput.datasources.csv.data import RowDataFactory
from zaimcsvconverter.inputtooutput.datasources.csv.records.gold_point_card_plus import GoldPointCardPlusRow
from zaimcsvconverter.models import Store


class TestGoldPointCardPlusRowData:
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
        used_date = "2018/7/3"
        used_store = "東京電力  電気料金等"
        used_card = "ご本人"
        payment_kind = "1回払い"
        number_of_division = ""
        scheduled_payment_month = "18/8"
        used_amount = "11402"
        unknown_1 = "11402"
        unknown_2 = "unknown 2"
        unknown_3 = "unknown 3"
        unknown_4 = "unknown 4"
        unknown_6 = "unknown 5"
        unknown_5 = "unknown 6"
        gold_point_card_plus_row_data = RowDataFactory(GoldPointCardPlusRowData).create(
            [
                used_date,
                used_store,
                used_card,
                payment_kind,
                number_of_division,
                scheduled_payment_month,
                used_amount,
                unknown_1,
                unknown_2,
                unknown_3,
                unknown_4,
                unknown_5,
                unknown_6,
            ]
        )
        assert gold_point_card_plus_row_data.used_card == used_card
        assert gold_point_card_plus_row_data.payment_kind == payment_kind
        assert gold_point_card_plus_row_data.number_of_division == number_of_division
        assert gold_point_card_plus_row_data.scheduled_payment_month == scheduled_payment_month
        assert gold_point_card_plus_row_data.used_amount == 11402
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
        "gold_point_card_plus_row_data, expected_date, expected_store_name_zaim, expected_is_row_to_skip",
        [
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC,
                datetime(2018, 7, 3, 0, 0, 0),
                "東京電力エナジーパートナー株式会社",
                False,
            ),
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP,
                datetime(2018, 7, 4, 0, 0, 0),
                "Amazon Japan G.K.",
                True,
            ),
            # Since アマゾン注文履歴フィルタ doesn't suppport return
            # see: https://github.com/furyutei/amzOrderHistoryFilter/blob/30ff80c6ea5194ec4b9ede986e30b80cbdd21355/src/js/amzOrderHistoryFilter.user.js#L4157 # noqa E501 pylint: disable=line-too-long
            (
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP_RETURN,
                datetime(2018, 12, 18, 0, 0, 0),
                "Amazon Japan G.K.",
                False,
            ),
        ],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_gold_point_card_plus")
    def test_init(
        gold_point_card_plus_row_data: GoldPointCardPlusRowData,
        expected_date: datetime,
        expected_store_name_zaim: str,
        expected_is_row_to_skip: bool,
    ) -> None:
        """Arguments should set into properties.

        :param GoldPointCardPlusRowData gold_point_card_plus_row_data:
        """
        row = GoldPointCardPlusRow(gold_point_card_plus_row_data)
        assert row.date == expected_date
        assert isinstance(row.store, Store)
        # pylint: disable=protected-access
        assert row.store.name == gold_point_card_plus_row_data.used_store
        assert row.store.name_zaim == expected_store_name_zaim
        assert row.is_row_to_skip == expected_is_row_to_skip
