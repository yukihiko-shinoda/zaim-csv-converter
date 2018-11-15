#!/usr/bin/env python

"""
This module implements constants which suitable module to belong is not defined.
"""

from __future__ import annotations
from enum import Enum
from typing import Dict, Any


class DirectoryCsv(Enum):
    """
    This class implements constant of directory of CSV.
    """
    CONVERT: str = './csvconverttable/'
    INPUT: str = './csvinput/'
    OUTPUT: str = './csvoutput/'


class FileCsvConvert(Enum):
    """
    This class implements constant of file of convert table CSV.
    """
    WAON: str = 'waon.csv'
    GOLD_POINT_CARD_PLUS: str = 'gold_point_card_plus.csv'
    MUFG: str = 'mufg.csv'

    @staticmethod
    def create(account: Account) -> FileCsvConvert:
        """
        This method creates Enum instance by Enum of Account.
        """
        return switch({
            Account.WAON: FileCsvConvert.WAON,
            Account.GOLD_POINT_CARD_PLUS: FileCsvConvert.GOLD_POINT_CARD_PLUS,
            Account.MUFG: FileCsvConvert.MUFG
        }, account)


class Account(Enum):
    """
    This class implements constant of account in Zaim.
    """
    WAON: int = 1
    GOLD_POINT_CARD_PLUS: int = 2
    MUFG: int = 3

    @staticmethod
    def create(account: FileCsvConvert) -> Account:
        """
        This method creates Enum instance by Enum of CSV convert file.
        """
        return switch({
            FileCsvConvert.WAON: Account.WAON,
            FileCsvConvert.GOLD_POINT_CARD_PLUS: Account.GOLD_POINT_CARD_PLUS,
            FileCsvConvert.MUFG: Account.MUFG,
        }, account)


def switch(dictionary: Dict, key: Enum) -> Any:
    """
    This method return value of dictionary. If key is not in dictionary, raise ValueError.
    """
    value = dictionary.get(key)
    if value is None:
        raise ValueError(f'"{key.name}" is not supported.')
    return value
