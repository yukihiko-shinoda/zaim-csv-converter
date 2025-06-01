"""This module implements database engine manager for unit testing."""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

import sqlalchemy
from sqlalchemy.engine.base import Engine

if TYPE_CHECKING:
    from types import TracebackType

    from sqlalchemy.orm import scoped_session
    from sqlalchemy.orm.session import Session


class DatabaseEngineManager(contextlib.AbstractContextManager[Engine]):
    """The database engine replacer for testing.

    This class implements context manager which replaces database engine from the one for development / production to
    the one for unit testing to keep data in the development / production database and inject new engine on every unit
    testing to run parallel.
    """

    def __init__(self, argument_scoped_session: scoped_session[Session]) -> None:
        self.scoped_session = argument_scoped_session
        self.engine = sqlalchemy.create_engine("sqlite://")

    def __enter__(self) -> Engine:
        self.scoped_session.configure(bind=self.engine)
        return self.engine

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        # Remove it, so that the next test gets a new Session()
        self.scoped_session.remove()
