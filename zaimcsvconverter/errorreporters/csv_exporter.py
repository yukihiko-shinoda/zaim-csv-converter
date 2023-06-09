"""This module implements CSV export."""
import csv
from pathlib import Path
from typing import Iterable, Union


class CsvExporter:
    """This class implements CSV export."""

    def __init__(self, directory_csv_output: Path) -> None:
        self.directory_csv_output = directory_csv_output

    def export(self, iterable: Iterable[list[Union[str, int]]], file_name: str) -> None:
        """This method exports iterable argument into CSV."""
        with (self.directory_csv_output / file_name).open("w", encoding="UTF-8", newline="\n") as file_error:
            writer_error = csv.writer(file_error)
            for error_row in iterable:
                writer_error.writerow(error_row)
