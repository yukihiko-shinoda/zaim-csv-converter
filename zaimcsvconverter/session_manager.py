#!/usr/bin/env python
from typing import NoReturn, Optional, List

from zaimcsvconverter import Session
from zaimcsvconverter.models import Store


class SessionManager(object):
    def __init__(self, session=Session()):
        self._session = session

    def __enter__(self):
        return self

    def save_stores(self, stores: List[Store]) -> NoReturn:
        with self._session.begin():
            self._session.add_all(stores)

    def find_store(self, store_kind, store_gold_point_card_plus):
        return self._session.query(Store).filter(
            Store.store_kind_id == store_kind,
            Store.name == store_gold_point_card_plus
        ).one()

    def __exit__(self, *exc):
        self._session.close()
