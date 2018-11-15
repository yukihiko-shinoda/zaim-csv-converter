#!/usr/bin/env python

"""
This module implements abstract income row model of MUFG bank CSV.
"""

from abc import abstractmethod

from zaimcsvconverter import CONFIG
from zaimcsvconverter.mufg.mufg_row import MufgRow


class MufgAbstractIncomeRow(MufgRow):
    """
    This class implements abstract income row model of MUFG bank CSV.
    """
    @abstractmethod
    def convert_to_zaim_row(self):
        pass

    @property
    @abstractmethod
    def _cash_flow_source_on_zaim(self) -> str:
        pass

    @property
    def _cash_flow_target_on_zaim(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def _amount(self) -> int:
        return self._deposit_amount
