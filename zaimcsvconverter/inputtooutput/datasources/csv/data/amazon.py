"""Zaim CSV Converter extended Amazon.co.jp CSV Data model."""

from datetime import datetime

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import amazon
from zaimcsvconverter.inputtooutput.datasources.csv.data import InputItemRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class AmazonRowData(amazon.AmazonRowData, InputItemRowData):
    """This class implements data class for wrapping list of Amazon.co.jp CSV row model."""

    @property
    def date(self) -> datetime:
        return self.ordered_date

    @property
    def item_name(self) -> str:
        return self.item_name_
