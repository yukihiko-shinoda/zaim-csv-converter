"""Tests for account.py"""
from enum import Enum
from pathlib import Path

import pytest

from zaimcsvconverter.account import Account


class FilePathConvertTable(Enum):
    """File path for test."""
    WAON = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\waon.csv')
    GOLD_POINT_CARD_PLUS = Path(
        'c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\gold_point_card_plus.csv')
    GOLD_POINT_CARD_PLUS_201912 = Path(
        'c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\gold_point_card_plus.csv')
    MUFG = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\mufg.csv')
    PASMO = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\sf_card_viewer.csv')
    AMAZON = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\amazon.csv')
    AMAZON_201911 = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\amazon.csv')
    VIEW_CARD = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\view_card.csv')

    @property
    def value(self) -> Path:
        """This method overwrite super method for type hint."""
        return super().value


class FilePathInput(Enum):
    """File path for test."""
    WAON = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\waon201804.csv')
    GOLD_POINT_CARD_PLUS = Path(
        'c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\gold_point_card_plus201804.csv')
    GOLD_POINT_CARD_PLUS_201912 = Path(
        'c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\gold_point_card_plus_201912_202004.csv')
    MUFG = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\mufg201804.csv')
    PASMO = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\pasmo201804.csv')
    AMAZON = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\amazon201804.csv')
    AMAZON_201911 = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\amazon_201911_201804.csv')
    VIEW_CARD = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\view_card_201804.csv')

    @property
    def value(self) -> Path:
        """This method overwrite super method for type hint."""
        return super().value


class TestAccount:
    """Tests for Account."""
    @staticmethod
    def test_create_by_path_csv_convert():
        """All accounts should have definition of convert table file name."""
        for account in Account:
            assert isinstance(Account.create_by_path_csv_convert(FilePathConvertTable[account.name].value), Account)

    @staticmethod
    def test_create_by_path_csv_input():
        """All accounts should have regex."""
        for account in Account:
            assert isinstance(Account.create_by_path_csv_input(FilePathInput[account.name].value), Account)

    @staticmethod
    def test_create_by_path_csv_input_error():
        """All accounts should have regex."""
        with pytest.raises(ValueError) as error:
            Account.create_by_path_csv_input(Path('test.csv'))
        assert str(error.value) == "can't detect account type by csv file name. Please confirm csv file name."
