"""This module implements SQLAlchemy session life cycle to prevent forgetting close."""
from types import TracebackType
from typing import Optional

from sqlalchemy.orm.session import Session as SQLAlchemySession

from zaimcsvconverter import Session


class SessionManager:
    """This class implements SQLAlchemy session life cycle to prevent forgetting close."""

    def __init__(self) -> None:
        self._session: SQLAlchemySession = Session()

    def __enter__(self) -> SQLAlchemySession:
        return self._session

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self._session.close()
