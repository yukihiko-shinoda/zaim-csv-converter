"""This module implements model of input CSV."""
from typing import Generic

from tests.testlibraries.csv_types import CSVWriter
from zaimcsvconverter.account import AccountContext
from zaimcsvconverter.datasources.data_source import DataSource
from zaimcsvconverter.inputcsvformats import TypeVarInputRow, TypeVarInputRowData
from zaimcsvconverter.inputtooutput.record_converter import RecordConverter


class InputData(Generic[TypeVarInputRowData, TypeVarInputRow]):
    """This class implements model of input CSV."""

    def __init__(
        self,
        datasource: DataSource[TypeVarInputRow, TypeVarInputRowData],
        account_context: AccountContext[TypeVarInputRowData, TypeVarInputRow],
    ):
        self.record_converter = RecordConverter(account_context.zaim_row_converter_factory)
        self.data_source = datasource

    def export_as_zaim_csv(self, writer_zaim: CSVWriter) -> None:
        """This method convert this csv into Zaim format CSV."""
        for input_record in self.data_source:
            zaim_row = self.record_converter.convert(input_record)
            writer_zaim.writerow(zaim_row.convert_to_list())
        self.data_source.raise_error_if_invalid()
