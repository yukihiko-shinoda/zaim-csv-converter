#!/usr/bin/env python
"""This module implements recipe for converting steps for WAON CSV."""
from __future__ import annotations
import re
from pathlib import Path
from typing import Type

from dataclasses import dataclass

from zaimcsvconverter.account_row import AccountRowData, AccountRow
from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_row import GoldPointCardPlusRowData, GoldPointCardPlusRow
from zaimcsvconverter.mufg.mufg_row import MufgRowData, MufgRow
from zaimcsvconverter.waon.waon_row import WaonRowData, WaonRow


@dataclass
class Recipe:
    """This class implements recipe for converting steps for WAON CSV."""
    csv_file: Path
    account_row_data_class: Type[AccountRowData]
    account_row_class: Type[AccountRow]
    is_including_header: bool = True
    encode: str = 'UTF-8'

    @staticmethod
    def create(path: Path) -> Recipe:
        """This function create correct setting instance by argument."""
        if re.search(r'.*waon.*\.csv', path.name):
            return Recipe(path, WaonRowData, WaonRow)
        if re.search(r'.*gold_point_card_plus.*\.csv', path.name):
            return Recipe(path, GoldPointCardPlusRowData, GoldPointCardPlusRow, False, 'shift_jis_2004')
        if re.search(r'.*mufg.*\.csv', path.name):
            return Recipe(path, MufgRowData, MufgRow, True, 'shift_jis_2004')
        raise TypeError('can\'t detect account type by csv file name. Please confirm csv file name.')
