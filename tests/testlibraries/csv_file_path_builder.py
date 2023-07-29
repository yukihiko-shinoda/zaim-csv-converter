"""This module implements fixtures file handler for CSV files."""
from pathlib import Path
from typing import Optional

from fixturefilehandler.file_paths import RelativeVacateFilePath


class CsvFilePathBuilder(RelativeVacateFilePath):
    """This class builds file path for config file.

    Default value is maybe suitable for standard directory structure of python project.
    """

    def __init__(
        self,
        target: Path = Path("export.csv"),
        backup: Optional[Path] = None,
        base: Optional[Path] = None,
        output: Path = Path("csvoutput"),
    ) -> None:
        if not base:
            base = Path.cwd()
        if backup is None:
            backup = Path(f"{target}.bak")
        super().__init__(target, backup, base / output)
