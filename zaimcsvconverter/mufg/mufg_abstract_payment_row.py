#!/usr/bin/env python

"""
This module implements abstract payment row model of MUFG bank CSV.
"""

from abc import abstractmethod

from zaimcsvconverter import CONFIG
from zaimcsvconverter.mufg.mufg_row import MufgRow


class MufgAbstractPaymentRow(MufgRow):
    """
    This class implements abstract payment row model of MUFG bank CSV.
    """
    @abstractmethod
    def convert_to_zaim_row(self):
        pass

    @property
    def _cash_flow_source_on_zaim(self) -> str:
        return CONFIG.mufg.account_name

    @property
    @abstractmethod
    def _cash_flow_target_on_zaim(self) -> str:
        pass

    @property
    def _amount(self) -> int:
        return self._payed_amount
