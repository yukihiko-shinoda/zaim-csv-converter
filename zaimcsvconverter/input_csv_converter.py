"""This module implements abstract converting steps for CSV."""
import csv
from pathlib import Path

from zaimcsvconverter import DirectoryCsv
from zaimcsvconverter.account import Account
from zaimcsvconverter.input_csv import InputData
from zaimcsvconverter.zaim_csv_format import ZaimCsvFormat


class InputCsvConverter:
    """This class implements abstract converting steps for CSV."""
    def __init__(self, path_csv_file: Path, directory_csv_output: Path = DirectoryCsv.OUTPUT.value):
        account = Account.create_by_path_csv_input(path_csv_file)
        csv_reader = account.value.csv_factory.create(path_csv_file)
        self.input_csv = InputData(csv_reader, account)
        self.path_to_output = directory_csv_output / path_csv_file.name

    def execute(self) -> None:
        """This method executes CSV convert steps."""
        with self.path_to_output.open('w', encoding='UTF-8', newline='\n') as file_zaim:
            writer_zaim = csv.writer(file_zaim)
            writer_zaim.writerow(ZaimCsvFormat.HEADER)
            self.input_csv.export_as_zaim_csv(writer_zaim)
