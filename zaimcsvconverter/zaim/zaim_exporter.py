"""This module implements model of input CSV."""
from abc import ABC, abstractmethod
import csv
from typing import TextIO

from zaimcsvconverter.datasources.data_source import DataSource
from zaimcsvconverter.inputtooutput.record_converter import RecordConverter
from zaimcsvconverter.zaim.zaim_csv_format import ZaimCsvFormat
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimExportOperator(ABC):
    @abstractmethod
    def output(self, zaim_row: ZaimRow) -> None:
        raise NotImplementedError


class ZaimCsvExportOperator(ZaimExportOperator):
    """Export operation of Zaim CSV."""

    def __init__(self, file_zaim: TextIO) -> None:
        writer_zaim = csv.writer(file_zaim)
        writer_zaim.writerow(ZaimCsvFormat.HEADER)
        self.writer_zaim = writer_zaim

    def output(self, zaim_row: ZaimRow) -> None:
        self.writer_zaim.writerow(zaim_row.convert_to_list())


class ZaimExporter:
    """This class implements model of input CSV."""

    def __init__(
        self,
        datasource: DataSource,
        record_converter: RecordConverter,
    ) -> None:
        self.record_converter = record_converter
        self.data_source = datasource

    def export(self, zaim_exporter: ZaimExportOperator) -> None:
        """This method convert this csv into Zaim format CSV."""
        for input_record in self.data_source:
            zaim_row = self.record_converter.convert(input_record)
            zaim_exporter.output(zaim_row)
        self.data_source.raise_error_if_invalid()
