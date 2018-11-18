#!/usr/bin/env python

"""
This module implements constants which suitable module to belong is not defined.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
import re
from typing import Type, TYPE_CHECKING, List, Union
from dataclasses import dataclass

from zaimcsvconverter.account.gold_point_card_plus import GoldPointCardPlusRowData, GoldPointCardPlusRow
from zaimcsvconverter.account.mufg import MufgRowData, MufgRow
from zaimcsvconverter.account.sf_card_viewer import SFCardViewerRowData, SFCardViewerRow
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
    encode: str = 'UTF-8'
    csv_header: Union[List[str], None] = None


class Account(Enum):
    """
    This class implements constant of account in Zaim.
    """
    WAON: AccountDependency = AccountDependency(
        1,
        'waon.csv',
        r'.*waon.*\.csv',
        WaonRowData,
        WaonRow,
        'UTF-8',
        ['取引年月日', '利用店舗', '利用金額（税込）', '利用区分', 'チャージ区分']
    )
    GOLD_POINT_CARD_PLUS: AccountDependency = AccountDependency(
        2,
        'gold_point_card_plus.csv',
        r'.*gold_point_card_plus.*\.csv',
        GoldPointCardPlusRowData,
        GoldPointCardPlusRow,
        'shift_jis_2004'
    )
    MUFG: AccountDependency = AccountDependency(
        3,
        'mufg.csv',
        r'.*mufg.*\.csv',
        MufgRowData,
        MufgRow,
        'shift_jis_2004',
        ['日付', '摘要', '摘要内容', '支払い金額', '預かり金額', '差引残高', 'メモ', '未資金化区分', '入払区分']
    )
    PASMO: AccountDependency = AccountDependency(
        4,
        'sp_card_viewer.csv',
        r'.*pasmo.*\.csv',
        SFCardViewerRowData,
        SFCardViewerRow,
        'shift_jis_2004',
        ['利用年月日', '定期', '鉄道会社名', '入場駅/事業者名', '定期', '鉄道会社名', '出場駅/降車場所', '利用額(円)', '残額(円)', 'メモ']
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
