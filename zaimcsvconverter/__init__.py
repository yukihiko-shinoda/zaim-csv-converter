"""This module implements default database settings."""

from enum import Enum
from pathlib import Path
from types import DynamicClassAttribute

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zaimcsvconverter.config import Config

# Reason: SWLAlchemy offcial documentation named as "Session".
# - Contextual/Thread-local Sessions | SQLAlchemy 2.0 Documentation
#   http://docs.sqlalchemy.org/en/latest/orm/contextual.html
Session = scoped_session(sessionmaker(bind=create_engine("sqlite://")))  # pylint: disable=invalid-name
CONFIG: Config = Config.create()


class DirectoryCsv(Enum):
    """This class implements constant of path to directory of CSV."""

    CONVERT = Path(__file__).parent.parent / "./csvconverttable/"
    INPUT = Path(__file__).parent.parent / "./csvinput/"
    OUTPUT = Path(__file__).parent.parent / "./csvoutput/"

    @DynamicClassAttribute
    def value(self) -> Path:
        """This method overwrite super method for type hint."""
        return super().value


PATH_FILE_CONFIG = Path(__file__).parent.parent / "config.yml"
