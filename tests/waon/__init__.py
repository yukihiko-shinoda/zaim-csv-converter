#!/usr/bin/env python

"""
This module implements test for waon module.
"""
from typing import NoReturn

from tests.database_test import StoreFactory
from zaimcsvconverter.enum import Account


def prepare_fixture() -> NoReturn:
    """
    This function prepare fixtures for this package.
    """
    StoreFactory(
        account=Account.WAON,
        list_row_store=['ファミリーマートかぶと町永代', 'ファミリーマート　かぶと町永代通り店'],
    )
    StoreFactory(
        account=Account.WAON,
        list_row_store=['板橋前野町', 'イオンスタイル　板橋前野町'],
    )
