"""Tests for account.py."""

from enum import Enum
from pathlib import Path
from types import DynamicClassAttribute

import pytest

from zaimcsvconverter.account import Account


class FilePathInput(Enum):
    """File path for test."""

    WAON = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\waon201804.csv")
    GOLD_POINT_CARD_PLUS = Path(
        "c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\gold_point_card_plus201804.csv",
    )
    GOLD_POINT_CARD_PLUS_201912 = Path(
        "c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\gold_point_card_plus_201912_202004.csv",
    )
    GOLD_POINT_CARD_PLUS_202009 = Path(
        "c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\gold_point_card_plus_202009_202009.csv",
    )
    MUFG = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\mufg201804.csv")
    PASMO = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\pasmo201804.csv")
    AMAZON = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\amazon201804.csv")
    AMAZON_201911 = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\amazon_201911_201804.csv")
    VIEW_CARD = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\view_card_201804.csv")
    SUICA = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\suica202003.csv")
    PAY_PAL = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\pay_pal201711.csv")
    SBI_SUMISHIN_NET_BANK = Path(
        "c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\sbi_sumishin_net_bank201711.csv",
    )
    PAY_PAY_CARD = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\pay_pay_card202208.csv")
    MOBILE_SUICA = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\mobile_suica202301.csv")

    @DynamicClassAttribute
    def value(self) -> Path:
        """This method overwrite super method for type hint."""
        return super().value


class TestAccount:
    """Tests for Account."""

    @staticmethod
    def test_create_by_path_csv_input() -> None:
        """All accounts should have regex."""
        for account in Account:
            assert isinstance(Account.create_by_path_csv_input(FilePathInput[account.name].value), Account)

    @staticmethod
    def test_create_by_path_csv_input_error() -> None:
        """All accounts should have regex."""
        with pytest.raises(
            ValueError,
            match=r"can\'t\sdetect\saccount\stype\sby\scsv\sfile\sname\.\sPlease\sconfirm\scsv\sfile\sname\.",
        ):
            Account.create_by_path_csv_input(Path("test.csv"))
