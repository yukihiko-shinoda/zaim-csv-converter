"""Optput model exporter to Zaim CSV."""
from __future__ import annotations
import contextlib
import csv
from pathlib import Path
from typing import Generator
from zaimcsvconverter.context_manager import ContextManager

from zaimcsvconverter.inputtooutput.output_model_exporter import OutputModelExporter
from zaimcsvconverter.zaim.zaim_csv_format import ZaimCsvFormat
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimCsvOutputModelExporter(OutputModelExporter[ZaimRow], ContextManager):
    """Export operation of Zaim CSV."""

    def __init__(self, path_to_output: Path) -> None:
        self.path_to_output = path_to_output
        self.writer_zaim = None

    def execute(self, output_row: ZaimRow) -> None:
        self.writer_zaim.writerow(output_row.convert_to_list())

    @contextlib.contextmanager
    def contextmanager(self) -> Generator[ZaimCsvOutputModelExporter, None, None]:
        with self.path_to_output.open("w", encoding="UTF-8", newline="\n") as file_zaim:
            self.writer_zaim = csv.writer(file_zaim)
            self.writer_zaim.writerow(ZaimCsvFormat.HEADER)
            yield self
