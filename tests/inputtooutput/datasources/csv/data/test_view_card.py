"""Tests for ViewCardRow."""
from datetime import datetime

from zaimcsvconverter.inputtooutput.datasources.csv.data import RowDataFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.view_card import ViewCardRowData


class TestViewCardRowData:
    """Tests for ViewCardRowData."""

    # Reason: asserting properties can't be short no more.
    # noinspection DuplicatedCode
    @staticmethod
    # pylint: disable=too-many-locals
    def test_init_and_property() -> None:
        """Tests following:

        - Property date should return datetime object.
        - Property store_date should return used_store.
        """
        used_date = "2020/03/31"
        used_place = "カード年会費"
        used_amount = "524"
        refund_amount = ""
        billing_amount = "524"
        number_of_division = "1回払"
        current_time_of_division = ""
        billing_amount_current_time = "524"
        local_currency_amount = ""
        currency_abbreviation = ""
        exchange_rate = ""
        view_card_row_data = RowDataFactory(ViewCardRowData).create(
            [
                used_date,
                used_place,
                used_amount,
                refund_amount,
                billing_amount,
                number_of_division,
                current_time_of_division,
                billing_amount_current_time,
                local_currency_amount,
                currency_abbreviation,
                exchange_rate,
            ]
        )
        assert view_card_row_data.date == datetime(2020, 3, 31, 0, 0)
        assert view_card_row_data.store_name == used_place
        assert view_card_row_data.billing_amount_current_time == 524
