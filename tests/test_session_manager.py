#!/usr/bin/env python
"""Tests for session manager."""
import pytest

from zaimcsvconverter import Session
from zaimcsvconverter.session_manager import SessionManager


class TestAccount:
    """Tests for session manager"""
    @pytest.fixture(autouse=True)
    def database_session(self):
        yield
        # Remove it, so that the next test gets a new Session()
        Session.remove()

    def test_convert_string_to_int_or_none(self):
        """Seesion should be non'active."""
        with SessionManager() as session:
            extracted_session = session
        assert not extracted_session.is_active
