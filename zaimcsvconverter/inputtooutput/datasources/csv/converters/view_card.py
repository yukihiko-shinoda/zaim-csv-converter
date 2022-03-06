"""Converter from VIEW CARD CSV data to record model."""
from zaimcsvconverter.inputcsvformats.view_card import ViewCardRow, ViewCardRowData
from zaimcsvconverter.inputtooutput.datasources.csv.converters import InputRowFactory


class ViewCardRowFactory(InputRowFactory[ViewCardRowData, ViewCardRow]):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: ViewCardRowData) -> ViewCardRow:  # type: ignore
        return ViewCardRow(input_row_data)
