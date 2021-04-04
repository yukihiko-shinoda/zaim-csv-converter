"""Tests for account.py"""
from enum import Enum
from pathlib import Path

import pytest

from zaimcsvconverter.account import Account


class FilePathInput(Enum):
    """File path for test."""

    WAON = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\waon201804.csv")
    GOLD_POINT_CARD_PLUS = Path(
        "c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\gold_point_card_plus201804.csv"
    )
    GOLD_POINT_CARD_PLUS_201912 = Path(
        "c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\gold_point_card_plus_201912_202004.csv"
    )
    GOLD_POINT_CARD_PLUS_202009 = Path(
        "c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\gold_point_card_plus_202009_202009.csv"
    )
    MUFG = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\mufg201804.csv")
    PASMO = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\pasmo201804.csv")
    AMAZON = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\amazon201804.csv")
    AMAZON_201911 = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\amazon_201911_201804.csv")
    VIEW_CARD = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\view_card_201804.csv")
    SUICA = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\suica202003.csv")
    PAY_PAL = Path("c:\\Users\\user\\workspace\\zaim-csv-converter\\csvinput\\pay_pal201711.csv")

    @property
    def value(self) -> Path:
        """This method overwrite super method for type hint."""
        return super().value


class TestAccount:
    """Tests for Account."""

    @staticmethod
    def test_create_by_path_csv_input():
        """All accounts should have regex."""
        for account in Account:
            assert isinstance(Account.create_by_path_csv_input(FilePathInput[account.name].value), Account)

    @staticmethod
    def test_create_by_path_csv_input_error():
        """All accounts should have regex."""
        with pytest.raises(ValueError) as error:
            Account.create_by_path_csv_input(Path("test.csv"))
        assert str(error.value) == "can't detect account type by csv file name. Please confirm csv file name."
