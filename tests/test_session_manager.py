"""Tests for session manager."""
import pytest

from zaimcsvconverter.session_manager import SessionManager


class TestAccount:
    """Tests for session manager."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("database_session_remove")
    def test_convert_string_to_int_or_none() -> None:
        """Session should be non'active."""
        with SessionManager() as session:
            extracted_session = session
        assert not extracted_session.is_active
