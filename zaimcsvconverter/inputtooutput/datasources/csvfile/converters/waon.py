"""Converter from WAON CSV data to record model."""

from zaimcsvconverter.data.waon import UseKind
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.waon import WaonRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.waon import WaonChargeRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.waon import WaonRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.waon import WaonRowToSkip
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.waon import WaonStoreRow


class WaonRowFactory(InputRowFactory[WaonRowData, WaonRow]):
    """This class implements factory to create WAON CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: WaonRowData) -> WaonRow:  # type: ignore[override]
        if input_row_data.use_kind in (
            UseKind.DOWNLOAD_POINT,
            UseKind.TRANSFER_WAON_UPLOAD,
            UseKind.TRANSFER_WAON_DOWNLOAD,
        ):
            return WaonRowToSkip(input_row_data)
        if input_row_data.use_kind in (UseKind.CHARGE, UseKind.AUTO_CHARGE):
            return WaonChargeRow(input_row_data)
        return WaonStoreRow(input_row_data)
