#!/usr/bin/env python

"""
This module implements transfer payment row model of MUFG bank CSV.
"""

from zaimcsvconverter.mufg.mufg_abstract_payment_row import MufgAbstractPaymentRow
from zaimcsvconverter.zaim.zaim_payment_row import ZaimPaymentRow
from zaimcsvconverter.zaim.zaim_transfer_row import ZaimTransferRow


class MufgTransferPaymentRow(MufgAbstractPaymentRow):
    """
    This class implements transfer payment row model of MUFG bank CSV.
    """
    def convert_to_zaim_row(self):
        if self._summary_content.transfer_target is None:
            return ZaimPaymentRow(self)
        return ZaimTransferRow(self)

    @property
    def _cash_flow_target_on_zaim(self) -> str:
        return self._summary_content.transfer_target
