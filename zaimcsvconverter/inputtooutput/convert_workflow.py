"""This module implements model of input CSV."""
from typing import Generic

from zaimcsvconverter.exceptions.invalid_input_csv_error import InvalidInputCsvError
from zaimcsvconverter.inputtooutput.converters import RecordConverter
from zaimcsvconverter.inputtooutput.datasources import DataSource
from zaimcsvconverter.inputtooutput.exporters import TypeVarOutputModelExporter


class ConvertWorkflow(Generic[TypeVarOutputModelExporter]):
    """This class implements model of input CSV."""

    def __init__(
        self,
        datasource: DataSource,
        record_converter: RecordConverter,
        output_model_exporter: TypeVarOutputModelExporter,
    ) -> None:
        self.data_source = datasource
        self.record_converter = record_converter
        self.output_model_exporter = output_model_exporter

    def execute(self) -> None:
        """This method convert this csv into Zaim format CSV."""
        with self.output_model_exporter:
            for input_record in self.data_source:
                output_record = self.record_converter.convert(input_record)
                self.output_model_exporter.execute(output_record)
        if self.data_source.is_invalid:
            raise InvalidInputCsvError(self.data_source, self.data_source.message)
