"""Tests for ViewCardRow."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.data.view_card import ViewCardRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.view_card import ViewCardNotStoreRow, ViewCardStoreRow
from zaimcsvconverter.models import Store


class TestViewCardNotStoreRow:
    """Tests for ViewCardNotStoreRow."""

    # pylint: disable=protected-access,too-many-arguments,unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        ("view_card_row_data", "expected_date", "expected_is_row_to_skip"),
        [
            (
                InstanceResource.ROW_DATA_VIEW_CARD_ITABASHI_STATION_AUTO_CHARGE,
                # Reason: Time is not used in this process.
                datetime(2020, 3, 21, 0, 0, 0),  # noqa: DTZ001
                True,
            ),
        ],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_view_card")
    def test_init(
        view_card_row_data: ViewCardRowData,
        expected_date: datetime,
        *,
        expected_is_row_to_skip: bool,
    ) -> None:
        """Arguments should set into properties.

        :type view_card_row_data: ViewCardRowData
        """
        # noinspection PyTypeChecker
        row = ViewCardNotStoreRow(view_card_row_data)
        assert row.date == expected_date
        assert row.is_row_to_skip == expected_is_row_to_skip


class TestViewCardStoreRow:
    """Tests for ViewCardStoreRow."""

    # pylint: disable=protected-access,too-many-arguments,unused-argument
    @pytest.mark.parametrize(
        ("view_card_row_data", "expected_date", "expected_store_name_zaim", "expected_is_row_to_skip"),
        [
            (
                InstanceResource.ROW_DATA_VIEW_CARD_ANNUAL_FEE,
                # Reason: Time is not used in this process.
                datetime(2020, 3, 31, 0, 0, 0),  # noqa: DTZ001
                "ビューカード　ビューカードセンター",
                False,
            ),
        ],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_view_card")
    def test_init(
        self,
        view_card_row_data: ViewCardRowData,
        expected_date: datetime,
        expected_store_name_zaim: str,
        *,
        expected_is_row_to_skip: bool,
    ) -> None:
        """Arguments should set into properties.

        :type view_card_row_data: ViewCardRowData
        """
        # noinspection PyTypeChecker
        row = ViewCardStoreRow(view_card_row_data)
        assert row.date == expected_date
        self.assert_store_and_item(
            row,
            view_card_row_data,
            expected_store_name_zaim,
            expected_is_row_to_skip=expected_is_row_to_skip,
        )

    def assert_store_and_item(
        self,
        row: ViewCardStoreRow,
        view_card_row_data: ViewCardRowData,
        expected_store_name_zaim: str,
        *,
        expected_is_row_to_skip: bool,
    ) -> None:
        """Asserts store and item."""
        assert isinstance(row.store, Store)
        # noinspection PyUnresolvedReferences
        assert row.store.name == view_card_row_data.used_place
        assert row.store.name_zaim == expected_store_name_zaim
        assert row.is_row_to_skip == expected_is_row_to_skip
