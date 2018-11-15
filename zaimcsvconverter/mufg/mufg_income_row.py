#!/usr/bin/env python

"""
This module implements income row model of MUFG bank CSV.
"""

from zaimcsvconverter import CONFIG
from zaimcsvconverter.mufg.mufg_abstract_income_row import MufgAbstractIncomeRow
from zaimcsvconverter.zaim.zaim_transfer_row import ZaimTransferRow


class MufgIncomeRow(MufgAbstractIncomeRow):
    """
    This class implements income row model of MUFG bank CSV.
    """
    def convert_to_zaim_row(self):
        return ZaimTransferRow(self)

    @property
    def _cash_flow_source_on_zaim(self) -> str:
        return CONFIG.mufg.transfer_account_name
