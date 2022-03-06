"""Converter from WAON CSV data to record model."""
from zaimcsvconverter.inputcsvformats.waon import UseKind, WaonChargeRow, WaonRow, WaonRowData
from zaimcsvconverter.inputtooutput.datasources.csv.converters import InputRowFactory


class WaonRowFactory(InputRowFactory[WaonRowData, WaonRow]):
    """This class implements factory to create WAON CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: WaonRowData) -> WaonRow:  # type: ignore
        if input_row_data.use_kind in (UseKind.CHARGE, UseKind.AUTO_CHARGE):
            return WaonChargeRow(input_row_data)
        return WaonRow(input_row_data)
