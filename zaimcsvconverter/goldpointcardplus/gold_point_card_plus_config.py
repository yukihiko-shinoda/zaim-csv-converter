#!/usr/bin/env python

"""
This module implements configuration for GOLD POINT CARD+.
"""


class GoldPointCardPlusConfig:
    """
    This class implements configuration for GOLD POINT CARD+.
    """
    KEY_ACCOUNT_NAME: str = 'account_name'
    KEY_PAYMENT_SOURCE: str = 'payment_source'

    def __init__(self, dictionary_config):
        self.account_name: str = dictionary_config.get(self.KEY_ACCOUNT_NAME)
        self.payment_source: str = dictionary_config.get(self.KEY_PAYMENT_SOURCE)
