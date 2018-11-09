#!/usr/bin/env python
import yaml

from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_config import GoldPointCardPlusConfig
from zaimcsvconverter.waon.waon_config import WaonConfig


class Config(object):
    KEY_WAON = 'waon'
    KEY_GOLD_POINT_CARD_PLUS = 'gold_point_card_plus'

    @property
    def waon(self):
        self.validate_load()
        return self._waon

    @property
    def gold_point_card_plus(self):
        self.validate_load()
        return self._gold_point_card_plus

    def __init__(self, file):
        self.file = file
        self.is_loaded = False
        self._waon = None
        self._gold_point_card_plus = None

    def load(self):
        with open(self.file, 'r', encoding='UTF-8') as yml:
            dictionary_config = yaml.load(yml)
            if self.KEY_WAON in dictionary_config:
                self._waon = WaonConfig(dictionary_config[self.KEY_WAON])
            if self.KEY_GOLD_POINT_CARD_PLUS in dictionary_config:
                self._gold_point_card_plus = GoldPointCardPlusConfig(dictionary_config[self.KEY_GOLD_POINT_CARD_PLUS])
        self.is_loaded = True

    def validate_load(self):
        if not self.is_loaded:
            raise RuntimeError('Config has not load. Please call load() function at first.')
