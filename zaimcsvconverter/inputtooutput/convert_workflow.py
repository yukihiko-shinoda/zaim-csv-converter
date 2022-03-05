"""This module implements model of input CSV."""
from abc import ABC, abstractmethod
import csv
from typing import Generic, TextIO

from zaimcsvconverter.datasources.data_source import DataSource
from zaimcsvconverter.inputtooutput.record_converter import RecordConverter
from zaimcsvconverter.zaim.zaim_csv_format import ZaimCsvFormat
from zaimcsvconverter.zaim.zaim_row import OutputRecord, TypeVarAbstractOutputRow, ZaimRow


class OutputModelExporter(Generic[TypeVarAbstractOutputRow], ABC):
    @abstractmethod
    def execute(self, output_row: TypeVarAbstractOutputRow) -> None:
        raise NotImplementedError


class ZaimCsvOutputModelExporter(OutputModelExporter[ZaimRow]):
    """Export operation of Zaim CSV."""

    def __init__(self, file_zaim: TextIO) -> None:
        writer_zaim = csv.writer(file_zaim)
        writer_zaim.writerow(ZaimCsvFormat.HEADER)
        self.writer_zaim = writer_zaim

    def execute(self, output_row: ZaimRow) -> None:
        self.writer_zaim.writerow(output_row.convert_to_list())


class ConvertWorkflow:
    """This class implements model of input CSV."""

    def __init__(
        self,
        datasource: DataSource,
        record_converter: RecordConverter,
    ) -> None:
        self.record_converter = record_converter
        self.data_source = datasource

    def export(self, output_model_exporter: OutputModelExporter[OutputRecord]) -> None:
        """This method convert this csv into Zaim format CSV."""
        for input_record in self.data_source:
            output_row = self.record_converter.convert(input_record)
            output_model_exporter.execute(output_row)
        self.data_source.raise_error_if_invalid()
