#!/usr/bin/env python

"""
This module implements constants which suitable module to belong is not defined.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
import re
from typing import Type, TYPE_CHECKING
from dataclasses import dataclass

from zaimcsvconverter.account.gold_point_card_plus import GoldPointCardPlusRowData, GoldPointCardPlusRow
from zaimcsvconverter.account.mufg import MufgRowData, MufgRow
from zaimcsvconverter.account.waon import WaonRowData, WaonRow
if TYPE_CHECKING:
    from zaimcsvconverter.account_row import AccountRowData, AccountRow


class DirectoryCsv(Enum):
    """
    This class implements constant of directory of CSV.
    """
    CONVERT: str = './csvconverttable/'
    INPUT: str = './csvinput/'
    OUTPUT: str = './csvoutput/'


@dataclass
class AccountDependency:
    """This class implements recipe for converting steps for WAON CSV."""
    id: int
    file_name_csv_convert: str
    regex_csv_file_name: str
    account_row_data_class: Type[AccountRowData]
    account_row_class: Type[AccountRow]
    is_including_header: bool = True
    encode: str = 'UTF-8'


class Account(Enum):
    """
    This class implements constant of account in Zaim.
    """
    WAON: AccountDependency = AccountDependency(
        1,
        'waon.csv',
        r'.*waon.*\.csv',
        WaonRowData,
        WaonRow
    )
    GOLD_POINT_CARD_PLUS: AccountDependency = AccountDependency(
        2,
        'gold_point_card_plus.csv',
        r'.*gold_point_card_plus.*\.csv',
        GoldPointCardPlusRowData,
        GoldPointCardPlusRow,
        False,
        'shift_jis_2004'
    )
    MUFG: AccountDependency = AccountDependency(
        3,
        'mufg.csv',
        r'.*mufg.*\.csv',
        MufgRowData,
        MufgRow,
        True,
        'shift_jis_2004'
    )

    @property
    def value(self) -> AccountDependency:
        """This method overwrite super method for type hint."""
        return super().value

    @staticmethod
    def create_by_path_csv_convert(path: Path) -> Account:
        """
        This method creates Enum instance by path to CSV convert file.
        """
        # noinspection PyUnusedLocal
        account: Account
        for account in Account:
            if path.name == account.value.file_name_csv_convert:
                return account
        raise ValueError('can\'t detect account type by csv file name. Please confirm csv file name.')

    @staticmethod
    def create_by_path_csv_input(path: Path) -> Account:
        """This function create correct setting instance by argument."""
        # noinspection PyUnusedLocal
        account: Account
        for account in Account:
            if re.search(account.value.regex_csv_file_name, path.name):
                return account
        raise ValueError('can\'t detect account type by csv file name. Please confirm csv file name.')

    @staticmethod
    def create_by_account_row(account_row: AccountRow) -> Account:
        """This function create correct setting instance by argument."""
        # noinspection PyUnusedLocal
        account: Account
        for account in Account:
            if isinstance(account_row, account.value.account_row_class):
                return account
        raise ValueError('can\'t detect account type by csv file name. Please confirm csv file name.')
