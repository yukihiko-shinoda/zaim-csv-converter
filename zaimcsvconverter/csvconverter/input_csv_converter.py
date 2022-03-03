"""This module implements abstract converting steps for CSV."""
from pathlib import Path

from zaimcsvconverter.account import Account, AccountContext
from zaimcsvconverter.csvconverter.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.csvconverter.zaim_exporter import ZaimCsvExportOperator, ZaimExporter
from zaimcsvconverter.datasources.csv import Csv
from zaimcsvconverter import DirectoryCsv
from zaimcsvconverter.inputcsvformats import InputRow, InputRowData


class InputCsvConverter:
    """This class implements abstract converting steps for CSV."""

    def __init__(self, path_csv_file: Path, directory_csv_output: Path = DirectoryCsv.OUTPUT.value):
        account_context: AccountContext[InputRowData, InputRow[InputRowData]] = Account.create_by_path_csv_input(
            path_csv_file
        ).value
        god_slayer = account_context.god_slayer_factory.create(path_csv_file)
        data_source_csv = Csv(god_slayer, CsvRecordProcessor(account_context))
        self.zaim_exporter = ZaimExporter(data_source_csv, account_context)
        self.path_to_output = directory_csv_output / path_csv_file.name

    def execute(self) -> None:
        """This method executes CSV convert steps."""
        with self.path_to_output.open("w", encoding="UTF-8", newline="\n") as file_zaim:
            self.zaim_exporter.export(ZaimCsvExportOperator(file_zaim))
