#!/usr/bin/env python


class GoldPointCardPlusConfig(object):
    KEY_ACCOUNT_NAME = 'account_name'
    KEY_PAYMENT_SOURCE = 'payment_source'

    def __init__(self, dictionary_config):
        self.account_name = dictionary_config.get(self.KEY_ACCOUNT_NAME)
        self.payment_source = dictionary_config.get(self.KEY_PAYMENT_SOURCE)
