"""This module implements abstract converting steps for CSV."""
import csv
from pathlib import Path

from zaimcsvconverter import DirectoryCsv
from zaimcsvconverter.input_csv import InputCsv
from zaimcsvconverter.zaim_csv_format import ZaimCsvFormat


class InputCsvConverter:
    """This class implements abstract converting steps for CSV."""
    def __init__(self, path_csv_file: Path, directory_csv_output: Path = DirectoryCsv.OUTPUT.value):
        self.input_csv = InputCsv(path_csv_file)
        self.path_to_output = directory_csv_output / path_csv_file.name

    def execute(self) -> None:
        """This method executes CSV convert steps."""
        with self.path_to_output.open('w', encoding='UTF-8', newline='\n') as file_zaim:
            writer_zaim = csv.writer(file_zaim)
            writer_zaim.writerow(ZaimCsvFormat.HEADER)
            self.input_csv.covert_to_zaim(writer_zaim)
