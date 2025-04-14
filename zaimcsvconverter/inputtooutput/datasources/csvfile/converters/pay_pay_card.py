"""Converter from PayPay Card CSV data to record model."""

from zaimcsvconverter.inputtooutput.datasources.csvfile.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.pay_pay_card import PayPayCardRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.pay_pay_card import PayPayCardRow


class PayPayCardRowFactory(InputRowFactory[PayPayCardRowData, PayPayCardRow]):
    """This class implements factory to create PayPay Card CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: PayPayCardRowData) -> PayPayCardRow:  # type: ignore[override]
        return PayPayCardRow(input_row_data)
