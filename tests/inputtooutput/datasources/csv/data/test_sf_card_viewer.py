"""Tests for sf_card_viewer.py."""
from datetime import datetime

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
            ]
        )
        assert sf_card_viewer_row_data.is_commuter_pass_enter == is_commuter_pass_enter
        assert sf_card_viewer_row_data.railway_company_name_enter == railway_company_name_enter
        assert sf_card_viewer_row_data.station_name_enter == station_name_enter
        assert sf_card_viewer_row_data.is_commuter_pass_exit == is_commuter_pass_exit
        assert sf_card_viewer_row_data.railway_company_name_exit == railway_company_name_exit
        assert sf_card_viewer_row_data.used_amount == 195
        assert sf_card_viewer_row_data.balance == balance
        assert sf_card_viewer_row_data.note == Note.EMPTY
        assert sf_card_viewer_row_data.date == datetime(2018, 11, 13, 0, 0)
        assert sf_card_viewer_row_data.store_name == station_name_exit
