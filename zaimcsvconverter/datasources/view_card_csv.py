"""This module implements VIEW CARD CSV with header model."""
from pathlib import Path

from godslayer.view_card_csv_reader import ViewCardCsvReader
from zaimcsvconverter.datasources.csv import CsvFactory
from zaimcsvconverter.datasources.csv_with_header import AbstractCsvWithHeader


class ViewCardCsv(AbstractCsvWithHeader):
    """This class implements analyzing process of VIEW CARD CSV."""
    def __init__(self, path_to_file: Path):
        super().__init__(ViewCardCsvReader(path_to_file))


class ViewCardCsvFactory(CsvFactory):
    """This class implements factory method for CsvWithHeaderReader."""
    def create(self, path_to_file: Path):
        return ViewCardCsv(path_to_file)
