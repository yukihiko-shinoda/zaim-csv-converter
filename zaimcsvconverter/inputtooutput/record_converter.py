"""RecordConverter."""
from zaimcsvconverter.datasources.data_source import AbstractInputRecord
from zaimcsvconverter.rowconverters import ZaimRowConverterFactory
from zaimcsvconverter.zaim.zaim_row import AbstractZaimRowFactory, ZaimRow


class RecordConverter:
    """Converts input record to output record."""

    def __init__(
        self, zaim_row_converter_factory: ZaimRowConverterFactory, zaim_row_factory: type[AbstractZaimRowFactory]
    ) -> None:
        self.zaim_row_converter_factory = zaim_row_converter_factory
        self.zaim_row_factory = zaim_row_factory

    def convert(self, input_record: AbstractInputRecord) -> ZaimRow:
        converter = self.zaim_row_converter_factory.create(input_record)
        return self.zaim_row_factory.create(converter)
