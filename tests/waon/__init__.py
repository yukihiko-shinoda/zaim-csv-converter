#!/usr/bin/env python
from tests.database_test import StoreFactory
from zaimcsvconverter.enum import Account


def prepare_fixture():
    StoreFactory(
        account=Account.WAON,
        list_row_store=['ファミリーマートかぶと町永代', 'ファミリーマート　かぶと町永代通り店'],
    )
    StoreFactory(
        account=Account.WAON,
        list_row_store=['板橋前野町', 'イオンスタイル　板橋前野町'],
    )
