"""Tests for session manager."""
import pytest

from zaimcsvconverter import Session
from zaimcsvconverter.session_manager import SessionManager


@pytest.fixture
def database_session():
    """This fixture remove created session after test."""
    yield
    # Remove it, so that the next test gets a new Session()
    Session.remove()


class TestAccount:
    """Tests for session manager"""

    # pylint: disable=unused-argument
    @staticmethod
    def test_convert_string_to_int_or_none(database_session):
        """Seesion should be non'active."""
        with SessionManager() as session:
            extracted_session = session
        assert not extracted_session.is_active
