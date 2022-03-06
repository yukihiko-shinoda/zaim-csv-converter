"""This module implements abstract converting steps for CSV."""
from pathlib import Path

from zaimcsvconverter.account import Account, AccountContext
from zaimcsvconverter import DirectoryCsv
from zaimcsvconverter.inputcsvformats import InputRow, InputRowData
from zaimcsvconverter.inputtooutput.convert_workflow import ConvertWorkflow
from zaimcsvconverter.inputtooutput.converters.recordtozaim import RecordToZaimConverter
from zaimcsvconverter.inputtooutput.datasources.csv import Csv
from zaimcsvconverter.inputtooutput.datasources.csv.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputtooutput.exporters.zaim.csv.zaim_csv_output_exporter import ZaimCsvOutputModelExporter


class CsvToCsvConverter:
    """This class implements abstract converting steps for CSV."""

    def __init__(self, path_csv_file: Path, directory_csv_output: Path = DirectoryCsv.OUTPUT.value):
        account_context: AccountContext[InputRowData, InputRow[InputRowData]] = Account.create_by_path_csv_input(
            path_csv_file
        ).value
        god_slayer = account_context.god_slayer_factory.create(path_csv_file)
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        data_source_csv = Csv(god_slayer, csv_record_processor)
        record_converter = RecordToZaimConverter(account_context.zaim_row_converter_factory)
        output_model_exporter = ZaimCsvOutputModelExporter(directory_csv_output / path_csv_file.name)
        self.convert_workflow = ConvertWorkflow(data_source_csv, record_converter, output_model_exporter)

    def execute(self) -> None:
        """This method executes CSV convert steps."""
        self.convert_workflow.execute()
