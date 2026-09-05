"""Converter from PayPay Card CSV data to record model (2025-05 format)."""

from zaimcsvconverter.inputtooutput.datasources.csvfile.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.pay_pay_card_202505 import PayPayCard202505RowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.pay_pay_card_202505 import PayPayCard202505Row


class PayPayCard202505RowFactory(InputRowFactory[PayPayCard202505RowData, PayPayCard202505Row]):
    """This class implements factory to create PayPay Card CSV row instance (2025-05 format)."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: PayPayCard202505RowData) -> PayPayCard202505Row:  # type: ignore[override]
        return PayPayCard202505Row(input_row_data)
