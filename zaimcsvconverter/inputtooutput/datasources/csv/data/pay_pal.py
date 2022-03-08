"""Zaim CSV Converter extended PayPal CSV Data model."""
from datetime import datetime

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import pay_pal
from zaimcsvconverter.inputtooutput.datasources.csv.data import InputStoreItemRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class PayPalRowData(pay_pal.PayPalRowData, InputStoreItemRowData):
    """This class implements data class for wrapping list of PayPal CSV row model."""

    @property
    def date(self) -> datetime:
        return self.date_

    @property
    def store_name(self) -> str:
        return self.name

    @property
    def item_name(self) -> str:
        return self.item_title
