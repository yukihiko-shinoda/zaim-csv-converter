"""Zaim CSV Converter extended PayPay Card CSV Data model (2025-05 format)."""

from datetime import datetime

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import pay_pay_card_202505
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import InputStoreRowData


@dataclass
class PayPayCard202505RowData(pay_pay_card_202505.PayPay202505RowData, InputStoreRowData):
    """This class implements data class for wrapping list of PayPay Card CSV row model (2025-05 format)."""

    @property
    def date(self) -> datetime:
        return self.used_cancelled_date

    @property
    def store_name(self) -> str:
        return self.used_store_name_item_name
