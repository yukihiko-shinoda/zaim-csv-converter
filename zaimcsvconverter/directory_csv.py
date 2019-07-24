"""This module defines path to directory of CSV."""
from enum import Enum
from pathlib import Path


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
