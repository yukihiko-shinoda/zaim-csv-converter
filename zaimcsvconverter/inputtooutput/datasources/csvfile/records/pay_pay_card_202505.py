"""This module implements row model of PayPay Card CSV (2025-05 format)."""

from __future__ import annotations

from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.pay_pay_card_202505 import PayPayCard202505RowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import InputStoreRow


class PayPayCard202505Row(InputStoreRow[PayPayCard202505RowData]):
    """This class implements row model of PayPay Card CSV (2025-05 format)."""

    def __init__(self, row_data: PayPayCard202505RowData) -> None:
        super().__init__(row_data, FileCsvConvert.PAY_PAY_CARD.value)
        self.used_amount: int = row_data.used_amount

    @property
    def validate(self) -> bool:
        return super().validate
