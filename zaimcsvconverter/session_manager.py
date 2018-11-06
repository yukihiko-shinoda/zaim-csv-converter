#!/usr/bin/env python
from typing import NoReturn, Optional

from zaimcsvconverter import Session
from zaimcsvconverter.models import WaonStore


class SessionManager(object):
    def __init__(self, session=Session()):
        self._session = session

    def __enter__(self):
        return self

    def save_waon_store(self, waon_store: WaonStore) -> NoReturn:
        with self._session.begin():
            self._session.add(waon_store)

    def find_waon_store(self, store_waon: str) -> Optional[WaonStore]:
        return self._session.query(WaonStore).filter(WaonStore.name == store_waon).one()

    def __exit__(self, *exc):
        self._session.close()
