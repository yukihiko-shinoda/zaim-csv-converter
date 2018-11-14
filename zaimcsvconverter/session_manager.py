#!/usr/bin/env python
from sqlalchemy.orm.session import Session as SQLAlchemySession

from zaimcsvconverter import Session


class SessionManager:
    def __init__(self):
        self._session: SQLAlchemySession = Session()

    def __enter__(self):
        return self._session

    def __exit__(self, *exc):
        self._session.close()
