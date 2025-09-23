"""This module implements default database settings."""

from enum import Enum
from pathlib import Path
from types import DynamicClassAttribute

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zaimcsvconverter.config import Config

Session = scoped_session(sessionmaker(bind=create_engine("sqlite://")))
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
