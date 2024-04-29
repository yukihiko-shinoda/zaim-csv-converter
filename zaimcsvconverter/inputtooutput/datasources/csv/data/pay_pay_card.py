"""Zaim CSV Converter extended PayPay Card CSV Data model."""

from datetime import datetime

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import pay_pay_card
from zaimcsvconverter.inputtooutput.datasources.csv.data import InputStoreRowData


@dataclass
class PayPayCardRowData(pay_pay_card.PayPayRowData, InputStoreRowData):
    """This class implements data class for wrapping list of PayPay Card CSV row model."""

    @property
    def date(self) -> datetime:
        return self.used_cancelled_date

    @property
    def store_name(self) -> str:
        return self.used_store_name_item_name
