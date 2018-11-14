#!/usr/bin/env python


class WaonConfig:
    KEY_ACCOUNT_NAME: str = 'account_name'
    KEY_AUTO_CHARGE_SOURCE: str = 'auto_charge_source'

    def __init__(self, dictionary_config):
        self.account_name: str = dictionary_config.get(self.KEY_ACCOUNT_NAME)
        self.auto_charge_source: str = dictionary_config.get(self.KEY_AUTO_CHARGE_SOURCE)
