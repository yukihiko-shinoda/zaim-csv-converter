"""This module implements fixtures file handler for CSV files."""

from __future__ import annotations

from pathlib import Path
from typing import Callable
from typing import Optional

from fixturefilehandler.file_paths import RelativeVacateFilePath


class CsvFilePathBuilder(RelativeVacateFilePath):
    """This class builds file path for config file.

    Default value is maybe suitable for standard directory structure of python project.
    """

    def __init__(
        self,
        target: Optional[Path] = None,
        backup: Optional[Path] = None,
        base: Optional[Path] = None,
        output: Optional[Path] = None,
    ) -> None:
        target = self.initialize(target, lambda: Path("export.csv"))
        backup = self.initialize(backup, lambda: Path(f"{target}.bak"))
        base = self.initialize(base, Path.cwd)
        output = self.initialize(output, lambda: Path("csvoutput"))
        super().__init__(target, backup, base / output)

    @staticmethod
    def initialize(optional: Optional[Path], default: Callable[[], Path]) -> Path:
        return optional if optional else default()
