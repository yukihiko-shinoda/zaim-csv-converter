"""This module defines path to directory of CSV."""
from enum import Enum
from pathlib import Path


class DirectoryCsv(Enum):
    """
    This class implements constant of path to directory of CSV.
    """
    CONVERT: Path = Path(__file__).parent.parent / './csvconverttable/'
    INPUT: Path = Path(__file__).parent.parent / './csvinput/'
    OUTPUT: Path = Path(__file__).parent.parent / './csvoutput/'
