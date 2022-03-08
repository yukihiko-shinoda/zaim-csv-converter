"""Converter from PayPal CSV data to record model."""
from zaimcsvconverter.inputtooutput.datasources.csv.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.pay_pal import PayPalRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.pay_pal import PayPalRow


class PayPalRowFactory(InputRowFactory[PayPalRowData, PayPalRow]):
    """This class implements factory to create Amazon.co.jp CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: PayPalRowData) -> PayPalRow:  # type: ignore
        return PayPalRow(input_row_data)
