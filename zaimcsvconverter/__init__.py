#!/usr/bin/env python

"""
This module implements default database settings.
"""

import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from zaimcsvconverter.config import Config


def call_session_maker(target_engine):
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


ENGINE = create_engine('sqlite://')
# ↓ To share same session with unit testing and inject new engine on every unit testing to run parallel
# pylint: disable=invalid-name
Session = None
if len(sys.argv) >= 1 and ('pytest' in sys.argv[0]):
    # pylint: disable=invalid-name
    Session = scoped_session(call_session_maker(ENGINE))
else:
    # pylint: disable=invalid-name
    Session = call_session_maker(ENGINE)
CONFIG: Config = Config()
