"""Tests for GoldPointCartPlusRow."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.data.gold_point_card_plus import GoldPointCardPlusRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.gold_point_card_plus import GoldPointCardPlusRow
from zaimcsvconverter.models import Store


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