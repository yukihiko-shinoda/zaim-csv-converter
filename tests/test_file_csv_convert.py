"""Tests for account.py"""
from enum import Enum
from pathlib import Path

from zaimcsvconverter.file_csv_convert import FileCsvConvert


class FilePathConvertTable(Enum):
    """File path for test."""
    WAON = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\waon.csv')
    GOLD_POINT_CARD_PLUS = Path(
        'c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\gold_point_card_plus.csv')
    MUFG = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\mufg.csv')
    SF_CARD_VIEWER = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\sf_card_viewer.csv')
    AMAZON = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\amazon.csv')
    VIEW_CARD = Path('c:\\Users\\user\\workspace\\zaim-csv-convereter\\csvconvettable\\view_card.csv')

    @property
    def value(self) -> Path:
        """This method overwrite super method for type hint."""
        return super().value


class TestFileCsvConvert:
    """Tests for FileCsvConvert."""
    @staticmethod
    def test_create_by_path_csv_convert():
        """All accounts should have definition of convert table file name."""
        for file_csv_convert in FileCsvConvert:
            assert isinstance(
                FileCsvConvert.create_by_path_csv_convert(FilePathConvertTable[file_csv_convert.name].value),
                FileCsvConvert
            )
