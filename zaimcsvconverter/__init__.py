"""This module implements default database settings."""
from enum import Enum
from pathlib import Path

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


class DirectoryCsv(Enum):
    """
    This class implements constant of path to directory of CSV.
    """
    CONVERT = Path(__file__).parent.parent / './csvconverttable/'
    INPUT = Path(__file__).parent.parent / './csvinput/'
    OUTPUT = Path(__file__).parent.parent / './csvoutput/'

    @property
    def value(self) -> Path:
        """This method overwrite super method for type hint."""
        return super().value


PATH_FILE_CONFIG = Path(__file__).parent.parent / 'config.yml'
