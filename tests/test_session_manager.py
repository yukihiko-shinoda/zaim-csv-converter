#!/usr/bin/env python
"""Tests for session manager."""
import unittest2 as unittest

from zaimcsvconverter.session_manager import SessionManager


class TestAccount(unittest.TestCase):
    """Tests for session manager"""
    def test_convert_string_to_int_or_none(self):
        """Seesion should be non'active."""
        with SessionManager() as session:
            extracted_session = session
        self.assertFalse(extracted_session.is_active)
