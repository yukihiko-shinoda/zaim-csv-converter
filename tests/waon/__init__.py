#!/usr/bin/env python

"""
This module implements test for waon module.
"""
from typing import NoReturn

from tests.database_test import StoreFactory
from zaimcsvconverter.account_dependency import Account
from zaimcsvconverter.models import StoreRowData


def prepare_fixture() -> NoReturn:
    """
    This function prepare fixtures for this package.
    """
    StoreFactory(
        account=Account.WAON,
        row_data=StoreRowData('ファミリーマートかぶと町永代', 'ファミリーマート　かぶと町永代通り店'),
    )
    StoreFactory(
        account=Account.WAON,
        row_data=StoreRowData('板橋前野町', 'イオンスタイル　板橋前野町'),
    )
