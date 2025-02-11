"""Optput model exporter to Zaim CSV."""

from __future__ import annotations

import contextlib
import csv
from typing import Optional, TYPE_CHECKING

from zaimcsvconverter.inputtooutput.exporters import OutputModelExporter
from zaimcsvconverter.inputtooutput.exporters.zaim.csvfile.zaim_csv_format import ZaimCsvFormat
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimRow

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

    from zaimcsvconverter.inputtooutput.exporters.zaim.csvfile.csv_types import CSVWriter


class ZaimCsvOutputModelExporter(OutputModelExporter[ZaimRow]):
    """Export operation of Zaim CSV."""

    def __init__(self, path_to_output: Path) -> None:
        self.path_to_output = path_to_output
        self.writer_zaim: Optional[CSVWriter] = None

    def execute(self, output_row: ZaimRow) -> None:
        # Reason: We won't to create if block since priority is efficiency than mypy type check.
        self.writer_zaim.writerow(output_row.convert_to_list())  # type: ignore[union-attr]

    @contextlib.contextmanager
    # Reason: Maybe there are no way to fix.
    # error: Return type "_GeneratorContextManager[ZaimCsvOutputModelExporter]" of "contextmanager"
    #   incompatible with return type "_GeneratorContextManager[<nothing>]" in supertype "ContextManager"
    def contextmanager(self) -> Generator[ZaimCsvOutputModelExporter, None, None]:  # type: ignore[override]
        with self.path_to_output.open("w", encoding="UTF-8", newline="\n") as file_zaim:
            self.writer_zaim = csv.writer(file_zaim)
            self.writer_zaim.writerow(ZaimCsvFormat.HEADER)
            yield self
