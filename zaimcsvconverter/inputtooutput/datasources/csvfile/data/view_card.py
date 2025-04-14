"""Zaim CSV Converter extended VIEW CARD CSV Data model."""

from datetime import datetime
import re

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import view_card
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import InputStoreRowData


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class ViewCardRowData(view_card.ViewCardRowData, InputStoreRowData):
    """This class implements data class for wrapping list of VIEW CARD CSV row model."""

    @property
    def date(self) -> datetime:
        return self.used_date

    @property
    def store_name(self) -> str:
        return self.used_place

    @property
    def is_suica(self) -> bool:
        """This property returns whether this store is Amazon.co.jp or not."""
        # Reason: Specification.
        is_auto_charge_mobile = bool(re.search(r"　オートチャージ(（モバイル）)?$", self.used_place))  # noqa: RUF001
        return is_auto_charge_mobile or self.used_place.startswith("Ｓｕｉｃａ（携帯決済）")  # noqa: RUF001
