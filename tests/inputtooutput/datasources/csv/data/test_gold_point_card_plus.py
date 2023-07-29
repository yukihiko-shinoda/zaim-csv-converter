"""Tests for GoldPointCartPlusRow."""
from datetime import datetime

from tests.testlibraries.assert_list import assert_each_properties
from zaimcsvconverter.inputtooutput.datasources.csv.data.gold_point_card_plus import GoldPointCardPlusRowData
from zaimcsvconverter.inputtooutput.datasources.csv.data import RowDataFactory


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
        expected_used_amount = 11402
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
            ],
        )
        assert_each_properties(
            gold_point_card_plus_row_data,
            [
                # Reason: Time is not used in this process.
                datetime(2018, 7, 3, 0, 0),  # noqa: DTZ001
                used_store,
                used_card,
                payment_kind,
                number_of_division,
                scheduled_payment_month,
                expected_used_amount,
                unknown_1,
                unknown_2,
                unknown_3,
                unknown_4,
                unknown_5,
                unknown_6,
            ],
        )
