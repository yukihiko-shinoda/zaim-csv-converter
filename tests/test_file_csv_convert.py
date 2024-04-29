"""Tests for account.py."""

from enum import Enum
import os
from pathlib import Path
from types import DynamicClassAttribute

from zaimcsvconverter.file_csv_convert import FileCsvConvert


class FilePathConvertTable(Enum):
    """File path for test."""

    WAON = Path("waon.csv")
    GOLD_POINT_CARD_PLUS = Path("gold_point_card_plus.csv")
    MUFG = Path("mufg.csv")
    SF_CARD_VIEWER = Path("sf_card_viewer.csv")
    AMAZON = Path("amazon.csv")
    VIEW_CARD = Path("view_card.csv")
    PAY_PAL_STORE = Path("pay_pal_store.csv")
    PAY_PAL_ITEM = Path("pay_pal_item.csv")
    SBI_SUMISHIN_NET_BANK = Path("sbi_sumishin_net_bank.csv")
    PAY_PAY_CARD = Path("pay_pay_card.csv")
    MOBILE_SUICA = Path("mobile_suica.csv")

    @DynamicClassAttribute
    def value(self) -> Path:
        """This method overwrite super method for type hint."""
        return super().value

    @property
    def path(self) -> Path:
        return (
            "c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable" / self.value
            if os.name == "nt"
            else "/root/workspace/zaim-csv-convereter/csvconvettable" / self.value
        )


class TestFileCsvConvert:
    """Tests for FileCsvConvert."""

    @staticmethod
    def test_create_by_path_csv_convert() -> None:
        """All accounts should have definition of convert table file name."""
        for file_csv_convert in FileCsvConvert:
            assert isinstance(
                FileCsvConvert.create_by_path_csv_convert(FilePathConvertTable[file_csv_convert.name].path),
                FileCsvConvert,
            )
