"""Tests for sf_card_viewer.py."""
from datetime import datetime

from tests.testlibraries.assert_list import assert_each_properties
from zaimcsvconverter.data.sf_card_viewer import Note
from zaimcsvconverter.inputtooutput.datasources.csv.data import RowDataFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.sf_card_viewer import SFCardViewerRowData


class TestSFCardViewerRowData:
    """Tests for SFCardViewerRowData."""

    @staticmethod
    def test_init_and_property() -> None:
        """Tests following:

        - Property date should return datetime object.
        - Property store_date should return used_store.
        """
        used_date = "2018/11/13"
        # Reason: Not hardcoded password.
        is_commuter_pass_enter = ""  # nosec
        railway_company_name_enter = "メトロ"
        station_name_enter = "六本木一丁目"
        # Reason: Not hardcoded password.
        is_commuter_pass_exit = ""  # nosec
        railway_company_name_exit = "メトロ"
        station_name_exit = "後楽園"
        used_amount = "195"
        balance = "3601"
        note = ""
        expected_used_amount = 195
        sf_card_viewer_row_data = RowDataFactory(SFCardViewerRowData).create(
            [
                used_date,
                is_commuter_pass_enter,
                railway_company_name_enter,
                station_name_enter,
                is_commuter_pass_exit,
                railway_company_name_exit,
                station_name_exit,
                used_amount,
                balance,
                note,
            ],
        )
        assert_each_properties(
            sf_card_viewer_row_data,
            [
                # Reason: Time is not used in this process.
                datetime(2018, 11, 13, 0, 0),  # noqa: DTZ001
                is_commuter_pass_enter,
                railway_company_name_enter,
                station_name_enter,
                is_commuter_pass_exit,
                railway_company_name_exit,
                station_name_exit,
                expected_used_amount,
                balance,
                Note.EMPTY,
            ],
        )
