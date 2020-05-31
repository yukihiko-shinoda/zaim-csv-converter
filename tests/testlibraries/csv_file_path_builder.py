"""This module implements fixtures file handler for CSV files."""
import os
from pathlib import Path

from fixturefilehandler.file_paths import RelativeVacateFilePath


class CsvFilePathBuilder(RelativeVacateFilePath):
    """
    This class builds file path for config file.
    Default value is maybe suitable for standard directory structure of python project.
    """

    def __init__(
        self,
        target: Path = Path("export.csv"),
        backup: Path = None,
        base: Path = Path(os.getcwd()),
        output: Path = Path("csvoutput"),
    ):
        if backup is None:
            backup = Path(f"{str(target)}.bak")
        super().__init__(target, backup, base / output)
