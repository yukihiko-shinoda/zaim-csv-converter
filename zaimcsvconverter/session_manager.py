"""This module implements SQLAlchemy session life cycle to prevent forgetting close."""
from sqlalchemy.orm.session import Session as SQLAlchemySession
from zaimcsvconverter import Session


class SessionManager:
    """
    This class implements SQLAlchemy session life cycle to prevent forgetting close.
    """
    def __init__(self):
        self._session: SQLAlchemySession = Session()

    def __enter__(self):
        return self._session

    def __exit__(self, *exc):
        self._session.close()
