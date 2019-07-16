"""This module implements default database settings."""
from sqlalchemy import create_engine
from zaimcsvconverter.config import Config
from zaimcsvconverter.session_factory import SessionFactory
ENGINE = create_engine('sqlite://')
# ↓ To share same session with unit testing and inject new engine on every unit testing to run parallel
# pylint: disable=invalid-name
Session = SessionFactory.create(ENGINE)
CONFIG: Config = Config()
