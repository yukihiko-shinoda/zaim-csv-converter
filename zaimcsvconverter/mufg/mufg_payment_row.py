#!/usr/bin/env python

"""
This module implements payment row model of MUFG bank CSV.
"""

from zaimcsvconverter import CONFIG
from zaimcsvconverter.mufg.mufg_abstract_payment_row import MufgAbstractPaymentRow
from zaimcsvconverter.zaim.zaim_transfer_row import ZaimTransferRow


class MufgPaymentRow(MufgAbstractPaymentRow):
    """
    This class implements payment row model of MUFG bank CSV.
    """
    def convert_to_zaim_row(self):
        return ZaimTransferRow(self)

    @property
    def _cash_flow_target_on_zaim(self) -> str:
        return CONFIG.mufg.transfer_account_name
