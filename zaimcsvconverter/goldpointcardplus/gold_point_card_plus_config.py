#!/usr/bin/env python


class GoldPointCardPlusConfig:
    KEY_ACCOUNT_NAME: str = 'account_name'
    KEY_PAYMENT_SOURCE: str = 'payment_source'

    def __init__(self, dictionary_config):
        self.account_name: str = dictionary_config.get(self.KEY_ACCOUNT_NAME)
        self.payment_source: str = dictionary_config.get(self.KEY_PAYMENT_SOURCE)
