"""This module implements database session factory class."""
import sys

# noinspection PyProtectedMember
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session


class SessionFactory:
    """This class implements method to create database session."""
    @classmethod
    def create(cls, engine: Engine):
        """This method creates database session."""
        if len(sys.argv) >= 1 and ('pytest' in sys.argv[0]):
            return scoped_session(cls.call_session_maker(engine))
        return cls.call_session_maker(engine)

    @classmethod
    def call_session_maker(cls, target_engine):
        """
        :param target_engine: Target engine to create session.
        :return: Created session factory.
        """
        return sessionmaker(
            bind=target_engine,
            # ↓ @ see https://stackoverflow.com/questions/32922210/why-does-a-query-invoke-a-auto-flush-in-sqlalchemy
            autoflush=False,
            # ↓ To use with-statement
            autocommit=True
        )
