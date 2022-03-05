"""This module implements model of input CSV."""
from zaimcsvconverter.datasources.data_source import DataSource
from zaimcsvconverter.inputtooutput.output_model_exporter import OutputModelExporter
from zaimcsvconverter.inputtooutput.record_converter import RecordConverter
from zaimcsvconverter.zaim.zaim_row import OutputRecord


class ConvertWorkflow:
    """This class implements model of input CSV."""

    def __init__(
        self,
        datasource: DataSource,
        record_converter: RecordConverter,
        output_model_exporter: OutputModelExporter[OutputRecord],
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
        self.data_source.raise_error_if_invalid()
