#!/usr/bin/env python

"""
This module implements transfer income row model of MUFG bank CSV.
"""

from zaimcsvconverter.mufg.mufg_abstract_income_row import MufgAbstractIncomeRow
from zaimcsvconverter.zaim.zaim_income_row import ZaimIncomeRow
from zaimcsvconverter.zaim.zaim_transfer_row import ZaimTransferRow


class MufgTransferIncomeRow(MufgAbstractIncomeRow):
    """
    This class implements transfer income row model of MUFG bank CSV.
    """
    def convert_to_zaim_row(self):
        if self._summary_content.transfer_target is None:
            return ZaimIncomeRow(self)
        return ZaimTransferRow(self)

    @property
    def _cash_flow_source_on_zaim(self) -> str:
        return self._summary_content.transfer_target
