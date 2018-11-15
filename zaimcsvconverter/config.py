#!/usr/bin/env python

"""
This module implements configuration.
"""

from typing import NoReturn

import yaml

from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_config import GoldPointCardPlusConfig
from zaimcsvconverter.mufg.mufg_config import MufgConfig
from zaimcsvconverter.waon.waon_config import WaonConfig


class Config:
    """
    This class implements configuration.
    """
    KEY_WAON: str = 'waon'
    KEY_GOLD_POINT_CARD_PLUS: str = 'gold_point_card_plus'
    KEY_MUFG: str = 'mufg'

    @property
    def waon(self) -> WaonConfig:
        """
        This property returns configuration of WAON.
        """
        self._validate_load()
        return self._waon

    @property
    def gold_point_card_plus(self) -> GoldPointCardPlusConfig:
        """
        This property returns configuration of GOLD POINT CARD+.
        """
        self._validate_load()
        return self._gold_point_card_plus

    @property
    def mufg(self) -> MufgConfig:
        """
        This property returns configuration of MUFG bank.
        """
        self._validate_load()
        return self._mufg

    def __init__(self, file: str):
        self.file: str = file
        self.is_loaded: bool = False
        self._waon: WaonConfig = None
        self._gold_point_card_plus: GoldPointCardPlusConfig = None
        self._mufg: MufgConfig = None

    def load(self) -> NoReturn:
        """
        This method load configuration from yaml file.
        """
        with open(self.file, 'r', encoding='UTF-8') as yml:
            dictionary_config = yaml.load(yml)
            if self.KEY_WAON in dictionary_config:
                self._waon = WaonConfig(dictionary_config[self.KEY_WAON])
            if self.KEY_GOLD_POINT_CARD_PLUS in dictionary_config:
                self._gold_point_card_plus = GoldPointCardPlusConfig(dictionary_config[self.KEY_GOLD_POINT_CARD_PLUS])
            if self.KEY_MUFG in dictionary_config:
                self._mufg = MufgConfig(dictionary_config[self.KEY_MUFG])
        self.is_loaded = True

    def _validate_load(self) -> NoReturn:
        if not self.is_loaded:
            raise RuntimeError('Config has not load. Please call load() function at first.')
