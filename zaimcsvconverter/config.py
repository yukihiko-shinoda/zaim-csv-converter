#!/usr/bin/env python

"""
This module implements configuration.
"""
from __future__ import annotations

import re
from abc import ABCMeta
from enum import Enum
from typing import Dict

import yaml
from dataclasses import dataclass, field


class AccountKey(Enum):
    """
    This class implements constant of account key for config.yml.
    """
    WAON: str = 'waon'
    GOLD_POINT_CARD_PLUS: str = 'gold_point_card_plus'
    MUFG: str = 'mufg'
    PASMO: str = 'pasmo'
    AMAZON: str = 'amazon'


class AccountConfig(metaclass=ABCMeta):
    """
    This class implements configuration for account.
    """
    @staticmethod
    def create(account_key: AccountKey, dict_account_config: dict) -> AccountConfig:
        """This method creates """
        account_config_class = {
            AccountKey.WAON: WaonConfig,
            AccountKey.GOLD_POINT_CARD_PLUS: GoldPointCardPlusConfig,
            AccountKey.MUFG: MufgConfig,
            AccountKey.PASMO: PasmoConfig,
            AccountKey.AMAZON: AmazonConfig,
        }.get(account_key)
        try:
            return account_config_class(**dict_account_config)
        except TypeError as error:
            matches = re.search(r"__init__\(\) got an unexpected keyword argument '(.*)'", str(error))
            if matches:
                raise TypeError(
                    f'Key "{account_key.value}.{matches.group(1)}" is undefined key.'
                    + f' Please confirm {Config.FILE_CONFIG}.'
                ) from error
            matches = re.search(r"__init__\(\) missing \d+ required positional argument: '(.*)'", str(error))
            if matches:
                raise TypeError(
                    f'Key "{account_key.value}.{matches.group(1)}" is required.'
                    + f' Please confirm {Config.FILE_CONFIG}.'
                ) from error
            raise error


@dataclass
class WaonConfig(AccountConfig):
    """
    This class implements configuration for WAON.
    """
    account_name: str
    auto_charge_source: str


@dataclass
class GoldPointCardPlusConfig(AccountConfig):
    """
    This class implements configuration for GOLD POINT CARD+.
    """
    account_name: str
    payment_source: str


@dataclass
class MufgConfig(AccountConfig):
    """
    This class implements configuration for MUFG bank.
    """
    account_name: str
    transfer_account_name: str


@dataclass
class PasmoConfig(AccountConfig):
    """
    This class implements configuration for PASMO.
    """
    account_name: str
    auto_charge_source: str
    skip_sales_goods_row: bool


@dataclass
class AmazonConfig(AccountConfig):
    """
    This class implements configuration for Amazon.co.jp.
    """
    store_name_zaim: str
    payment_account_name: str


@dataclass
class Config:
    """
    This class implements configuration wrapping.
    """
    waon: WaonConfig = None
    gold_point_card_plus: GoldPointCardPlusConfig = None
    mufg: MufgConfig = None
    pasmo: PasmoConfig = None
    amazon: AmazonConfig = None
    FILE_CONFIG: str = field(default='./config.yml', init=False)

    def load(self):
        """This method creates instance by dict."""
        with open(Config.FILE_CONFIG, 'r', encoding='UTF-8') as yml:
            dictionary_config = yaml.load(yml)
        account_config: Dict[str, AccountConfig] = {}
        for key_string, dict_account_config in dictionary_config.items():
            key_enum = AccountKey(key_string)
            if key_enum is None:
                raise ValueError(f'Key "{key_string}" is undefined key. Please confirm {Config.FILE_CONFIG}.')
            account_config[key_string] = AccountConfig.create(key_enum, dict_account_config)
        self.__dict__.update(Config(**account_config).__dict__)
