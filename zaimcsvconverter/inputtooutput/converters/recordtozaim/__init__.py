"""RecordConverter from input to Zaim."""
from zaimcsvconverter.inputtooutput.converters import RecordConverter
from zaimcsvconverter.inputtooutput.datasources import AbstractInputRecord
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimRow, ZaimRowFactory
from zaimcsvconverter.rowconverters import ZaimRowConverterFactory


class RecordToZaimConverter(RecordConverter):
    """Converts input record to output record."""

    def __init__(self, zaim_row_converter_factory: ZaimRowConverterFactory) -> None:
        self.zaim_row_converter_factory = zaim_row_converter_factory

    def convert(self, input_record: AbstractInputRecord) -> ZaimRow:
        converter = self.zaim_row_converter_factory.create(input_record)
        return ZaimRowFactory.create(converter)
