"""Zaim CSV Converter extended Mobile Suica CSV Data model."""
from datetime import datetime

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import mobile_suica
from zaimcsvconverter.inputtooutput.datasources.csv.data import InputStoreRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class MobileSuicaRowData(mobile_suica.MobileSuicaRowData, InputStoreRowData):
    """This class implements data class for wrapping list of Mobile Suica CSV row model."""

    @property
    def date(self) -> datetime:
        return self.month_date

    @property
    def store_name(self) -> str:
        return self.used_place_2 if self.has_kind_2 else self.used_place_1

    @property
    def has_kind_2(self) -> bool:
        """This property returns whether this row has kind 2."""
        return self.kind_2 is not mobile_suica.Kind2.EMPTY

    @property
    def has_used_place_1(self) -> bool:
        """This property returns whether this row has used place 1."""
        return bool(self.used_place_1)

    @property
    def is_used_in_mobile(self) -> bool:
        """This property returns whether this row has used place 1."""
        return self.used_place_1 == "モバイル"

    @property
    def first_record(self) -> bool:
        """This property returns whether this row has used place 1."""
        return not self.has_kind_2 and self.is_used_in_mobile and self.deposit_used_amount is None
