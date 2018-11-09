#!/usr/bin/env python


class WaonConfig(object):
    KEY_ACCOUNT_NAME = 'account_name'
    KEY_AUTO_CHARGE_SOURCE = 'auto_charge_source'

    def __init__(self, dictionary_config):
        self.account_name = dictionary_config.get(self.KEY_ACCOUNT_NAME)
        self.auto_charge_source = dictionary_config.get(self.KEY_AUTO_CHARGE_SOURCE)
