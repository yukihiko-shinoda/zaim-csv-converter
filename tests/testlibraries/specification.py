"""This module implements specification of production code."""
from pathlib import Path


class Specification:
    """This class implements specification of production code."""

    PATH_DIRECTORY_CSV_CONVERT_TABLE = Path(__file__).parent.parent.parent / "csvconverttable"
    PATH_DIRECTORY_CSV_INPUT = Path(__file__).parent.parent.parent / "csvinput"
    PATH_DIRECTORY_CSV_OUTPUT = Path(__file__).parent.parent.parent / "csvoutput"
