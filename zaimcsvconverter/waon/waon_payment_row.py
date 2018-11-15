#!/usr/bin/env python

"""
This module implements payment row model of WAON.
"""

from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_payment_row import ZaimPaymentRow


class WaonPaymentRow(WaonRow):
    """
    This class implements payment row model of WAON.
    """
    def convert_to_zaim_row(self) -> ZaimPaymentRow:
        return ZaimPaymentRow(self)
