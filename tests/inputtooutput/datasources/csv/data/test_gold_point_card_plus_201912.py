"""Tests for GoldPointCartPlusRow."""

from datetime import datetime

from zaimcsvconverter.inputtooutput.datasources.csv.data.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912RowData,
)
from zaimcsvconverter.inputtooutput.datasources.csv.data import RowDataFactory


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
        expected_payed_amount = 66
        gold_point_card_plus_row_data = RowDataFactory(GoldPointCardPlus201912RowData).create(
            [used_date, used_store, used_amount, number_of_division, current_time_of_division, payed_amount, others],
        )
        # Reason: Time is not used in this process.
        assert gold_point_card_plus_row_data.date == datetime(2019, 11, 3, 0, 0)  # noqa: DTZ001
        assert gold_point_card_plus_row_data.store_name == used_store
        assert gold_point_card_plus_row_data.payed_amount == expected_payed_amount
