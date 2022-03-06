"""Converter from Amazon.co.jp CSV data to record model."""
from zaimcsvconverter.inputcsvformats.amazon import AmazonRow, AmazonRowData
from zaimcsvconverter.inputtooutput.datasources.csv.converters import InputRowFactory


class AmazonRowFactory(InputRowFactory[AmazonRowData, AmazonRow]):
    """This class implements factory to create Amazon.co.jp CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: AmazonRowData) -> AmazonRow:  # type: ignore
        return AmazonRow(input_row_data)
