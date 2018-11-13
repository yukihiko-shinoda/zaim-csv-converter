#!/usr/bin/env python
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from zaimcsvconverter.config import Config


def call_session_maker(target_engine):
    return sessionmaker(
        bind=target_engine,
        # ↓ @ see https://stackoverflow.com/questions/32922210/why-does-a-query-invoke-a-auto-flush-in-sqlalchemy
        autoflush=False,
        # ↓ To use with-statement
        autocommit=True
    )


engine = create_engine('sqlite://')
# ↓ To share same session with unittest and inject new engine on every unittest to run parallel
# noinspection Pylint
Session = None
if len(sys.argv) >= 1 and 'unittest' in sys.argv[0]:
    # noinspection Pylint
    Session = scoped_session(call_session_maker(engine))
else:
    # noinspection Pylint
    Session = call_session_maker(engine)
FILE_CONFIG: str = './config.yml'
CONFIG: Config = Config(FILE_CONFIG)
