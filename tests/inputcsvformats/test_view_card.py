"""Tests for ViewCardRow."""
from datetime import datetime

import pytest
from sqlalchemy.orm.exc import NoResultFound

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputcsvformats import RowDataFactory
from zaimcsvconverter.inputcsvformats.view_card import ViewCardRow, ViewCardRowData, ViewCardRowFactory
from zaimcsvconverter.models import Store


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


class TestViewCardRow:
    """Tests for ViewCardRow."""

    # pylint: disable=protected-access,too-many-arguments,unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "view_card_row_data, expected_date, expected_store_name_zaim, expected_is_row_to_skip",
        [
            (
                InstanceResource.ROW_DATA_VIEW_CARD_ITABASHI_STATION_AUTO_CHARGE,
                datetime(2020, 3, 21, 0, 0, 0),
                None,
                True,
            ),
            (
                InstanceResource.ROW_DATA_VIEW_CARD_ANNUAL_FEE,
                datetime(2020, 3, 31, 0, 0, 0),
                "ビューカード　ビューカードセンター",
                False,
            ),
        ],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_view_card")
    def test_init(
        view_card_row_data: ViewCardRowData,
        expected_date: datetime,
        expected_store_name_zaim: str,
        expected_is_row_to_skip: bool,
    ) -> None:
        """Arguments should set into properties.

        :type view_card_row_data: ViewCardRowData
        """
        # noinspection PyTypeChecker
        row = ViewCardRow(view_card_row_data)
        assert row.date == expected_date
        # pylint: disable=protected-access
        if expected_store_name_zaim is None:
            with pytest.raises(NoResultFound):
                # pylint: disable=unused-variable
                store_name = row.store  # noqa
        else:
            assert isinstance(row.store, Store)
            # noinspection PyUnresolvedReferences
            assert row.store.name == view_card_row_data.used_place
            assert row.store.name_zaim == expected_store_name_zaim
        assert row.is_row_to_skip == expected_is_row_to_skip


class TestViewCardRowFactory:
    """Tests for GoldPointCardPlusRowFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize("argument, expected", [(InstanceResource.ROW_DATA_VIEW_CARD_ANNUAL_FEE, ViewCardRow)])
    @pytest.mark.usefixtures("database_session_stores_view_card")
    def test_create(argument: ViewCardRowData, expected: type[ViewCardRow]) -> None:
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        view_card_row = ViewCardRowFactory().create(argument)
        assert isinstance(view_card_row, expected)
