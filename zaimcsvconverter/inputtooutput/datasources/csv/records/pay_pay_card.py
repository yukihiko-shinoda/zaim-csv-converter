"""This module implements row model of PayPay Card CSV."""

from __future__ import annotations

from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csv.data.pay_pay_card import PayPayCardRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputStoreRow


class PayPayCardRow(InputStoreRow[PayPayCardRowData]):
    """This class implements row model of PayPay Card CSV."""

    def __init__(self, row_data: PayPayCardRowData) -> None:
        super().__init__(row_data, FileCsvConvert.PAY_PAY_CARD.value)
        self.used_amount: int = row_data.used_amount

    @property
    def validate(self) -> bool:
        return super().validate
