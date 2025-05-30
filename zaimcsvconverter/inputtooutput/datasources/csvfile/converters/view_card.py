"""Converter from VIEW CARD CSV data to record model."""

from zaimcsvconverter.inputtooutput.datasources.csvfile.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.view_card import ViewCardRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.view_card import ViewCardNotStoreRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.view_card import ViewCardRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.view_card import ViewCardStoreRow


class ViewCardRowFactory(InputRowFactory[ViewCardRowData, ViewCardRow]):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: ViewCardRowData) -> ViewCardRow:  # type: ignore[override]
        if input_row_data.is_suica:
            return ViewCardNotStoreRow(input_row_data)
        return ViewCardStoreRow(input_row_data)
