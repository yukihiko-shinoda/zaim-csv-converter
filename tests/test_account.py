#!/usr/bin/env python
"""Tests for account.py"""
from enum import Enum
from pathlib import Path

from zaimcsvconverter.account import Account


class FilePathConvertTable(Enum):
    """File path for test."""
    WAON: Path = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\waon.csv')
    GOLD_POINT_CARD_PLUS: Path = Path(
        'c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\gold_point_card_plus.csv')
    MUFG: Path = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\mufg.csv')
    PASMO: Path = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\sf_card_viewer.csv')
    AMAZON: Path = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\amazon.csv')


class FilePathInput(Enum):
    """File path for test."""
    WAON: Path = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\waon201804.csv')
    GOLD_POINT_CARD_PLUS: Path = Path(
        'c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\gold_point_card_plus201804.csv')
    MUFG: Path = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\mufg201804.csv')
    PASMO: Path = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\pasmo201804.csv')
    AMAZON: Path = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvinput\\amazon201804.csv')


class TestAccount:
    """Tests for Account."""
    def test_create_by_path_csv_convert(self):
        """All accounts should have definition of convert table file name."""
        for account in Account:
            assert isinstance(Account.create_by_path_csv_convert(FilePathConvertTable[account.name].value), Account)

    def test_create_by_path_csv_input(self):
        """All accounts should have regex."""
        for account in Account:
            assert isinstance(Account.create_by_path_csv_input(FilePathInput[account.name].value), Account)
