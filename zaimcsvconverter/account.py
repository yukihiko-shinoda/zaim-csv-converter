#!/usr/bin/env python

"""
This module implements constants which suitable module to belong is not defined.
"""
from __future__ import annotations

import re
from enum import Enum
from pathlib import Path

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_dependency import AccountDependency
from zaimcsvconverter.inputcsvformats.amazon import AmazonRowData, AmazonRowFactory
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRowData, GoldPointCardPlusRowFactory
from zaimcsvconverter.inputcsvformats.mufg import MufgRowData, MufgRowFactory
from zaimcsvconverter.inputcsvformats.sf_card_viewer import SFCardViewerRowData, SFCardViewerRowFactory
from zaimcsvconverter.inputcsvformats.waon import WaonRowData, WaonRowFactory
from zaimcsvconverter.models import Store, Item


class Account(Enum):
    """
    This class implements constant of account in Zaim.
    """
    WAON: AccountDependency = AccountDependency(
        1,
        'waon.csv',
        r'.*waon.*\.csv',
        Store,
        WaonRowData,
        WaonRowFactory(),
        'UTF-8',
        ['取引年月日', '利用店舗', '利用金額（税込）', '利用区分', 'チャージ区分']
    )
    GOLD_POINT_CARD_PLUS: AccountDependency = AccountDependency(
        2,
        'gold_point_card_plus.csv',
        r'.*gold_point_card_plus.*\.csv',
        Store,
        GoldPointCardPlusRowData,
        GoldPointCardPlusRowFactory(),
        'shift_jis_2004'
    )
    MUFG: AccountDependency = AccountDependency(
        3,
        'mufg.csv',
        r'.*mufg.*\.csv',
        Store,
        MufgRowData,
        MufgRowFactory(),
        'shift_jis_2004',
        ['日付', '摘要', '摘要内容', '支払い金額', '預かり金額', '差引残高', 'メモ', '未資金化区分', '入払区分']
    )
    PASMO: AccountDependency = AccountDependency(
        4,
        'sf_card_viewer.csv',
        r'.*pasmo.*\.csv',
        Store,
        SFCardViewerRowData,
        SFCardViewerRowFactory(lambda: CONFIG.pasmo),
        'shift_jis_2004',
        ['利用年月日', '定期', '鉄道会社名', '入場駅/事業者名', '定期', '鉄道会社名', '出場駅/降車場所', '利用額(円)', '残額(円)', 'メモ']
    )
    AMAZON: AccountDependency = AccountDependency(
        5,
        'amazon.csv',
        r'.*amazon.*\.csv',
        Item,
        AmazonRowData,
        AmazonRowFactory(),
        'utf-8-sig',
        [
            '注文日', '注文番号', '商品名', '付帯情報', '価格', '個数', '商品小計', '注文合計',
            'お届け先', '状態', '請求先', '請求額', 'クレカ請求日', 'クレカ請求額', 'クレカ種類',
            '注文概要URL', '領収書URL', '商品URL'
        ]
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
