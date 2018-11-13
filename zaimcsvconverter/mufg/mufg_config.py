#!/usr/bin/env python


class MufgConfig(object):
    KEY_ACCOUNT_NAME: str = 'account_name'
    KEY_TRANSFER_ACCOUNT_NAME: str = 'transfer_account_name'

    def __init__(self, dictionary_config):
        self.account_name: str = dictionary_config.get(self.KEY_ACCOUNT_NAME)
        self.transfer_account_name: str = dictionary_config.get(self.KEY_TRANSFER_ACCOUNT_NAME)
