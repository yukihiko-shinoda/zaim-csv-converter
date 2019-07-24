"""This module implements default database settings."""
from sqlalchemy import create_engine
# noinspection PyProtectedMember
from sqlalchemy.orm import sessionmaker, scoped_session

from zaimcsvconverter.config import Config
# pylint: disable=invalid-name
Session = scoped_session(sessionmaker(
    bind=create_engine('sqlite://'),
    # ↓ @ see https://stackoverflow.com/questions/32922210/why-does-a-query-invoke-a-auto-flush-in-sqlalchemy
    autoflush=False,
    # ↓ To use with-statement
    autocommit=True
))
CONFIG: Config = Config()
