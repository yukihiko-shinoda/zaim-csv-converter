"""RecordConverter."""
from returns.primitives.hkt import Kind1

from zaimcsvconverter.inputcsvformats import TypeVarInputRow, TypeVarInputRowData
from zaimcsvconverter.rowconverters import ZaimRowConverterFactory
from zaimcsvconverter.zaim.zaim_row import ZaimRow, ZaimRowFactory


class RecordConverter:
    """Converts input record to output record."""

    def __init__(
        self, zaim_row_converter_factory: ZaimRowConverterFactory[TypeVarInputRow, TypeVarInputRowData]
    ) -> None:
        self.zaim_row_converter_factory = zaim_row_converter_factory

    def convert(self, input_record: Kind1[TypeVarInputRow, TypeVarInputRowData]) -> ZaimRow:
        converter = self.zaim_row_converter_factory.create(input_record)
        return ZaimRowFactory.create(converter)
