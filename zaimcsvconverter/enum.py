#!/usr/bin/env python
from __future__ import annotations
from enum import Enum
from typing import Dict, Any


class DirectoryCsv(Enum):
    CONVERT: str = './csvconverttable/'
    INPUT: str = './csvinput/'
    OUTPUT: str = './csvoutput/'


class FileCsvConvert(Enum):
    WAON: str = 'waon.csv'
    GOLD_POINT_CARD_PLUS: str = 'gold_point_card_plus.csv'
    MUFG: str = 'mufg.csv'

    @staticmethod
    def create(account: Account) -> FileCsvConvert:
        return switch({
            Account.WAON: FileCsvConvert.WAON,
            Account.GOLD_POINT_CARD_PLUS: FileCsvConvert.GOLD_POINT_CARD_PLUS,
            Account.MUFG: FileCsvConvert.MUFG
        }, account)


class Account(Enum):
    WAON: int = 1
    GOLD_POINT_CARD_PLUS: int = 2
    MUFG: int = 3

    @staticmethod
    def create(account: FileCsvConvert) -> Account:
        return switch({
            FileCsvConvert.WAON: Account.WAON,
            FileCsvConvert.GOLD_POINT_CARD_PLUS: Account.GOLD_POINT_CARD_PLUS,
            FileCsvConvert.MUFG: Account.MUFG,
        }, account)


def switch(dictionary: Dict, key: Enum) -> Any:
    value = dictionary.get(key)
    if value is None:
        raise ValueError(f'"{key.name}" is not supported.')
    return value
