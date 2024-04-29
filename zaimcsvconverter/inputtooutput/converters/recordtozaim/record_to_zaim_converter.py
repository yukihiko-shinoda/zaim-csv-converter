"""RecordConverter from input to Zaim."""

from pathlib import Path

from zaimcsvconverter.inputtooutput.converters import RecordConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimRowConverterFactory, ZaimRowFactory
from zaimcsvconverter.inputtooutput.datasources import AbstractInputRecord
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimRow


class RecordToZaimConverter(RecordConverter):
    """Converts input record to output record."""

    def __init__(self, zaim_row_converter_factory: ZaimRowConverterFactory, path_csv_file: Path) -> None:
        self.zaim_row_converter_factory = zaim_row_converter_factory
        self.path_csv_file = path_csv_file

    def convert(self, input_record: AbstractInputRecord) -> ZaimRow:
        converter = self.zaim_row_converter_factory.create(input_record, self.path_csv_file)
        return ZaimRowFactory.create(converter)
