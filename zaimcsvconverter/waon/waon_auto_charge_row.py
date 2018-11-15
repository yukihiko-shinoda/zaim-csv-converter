#!/usr/bin/env python

"""
This module implements auto charge row model of WAON.
"""

from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_transfer_row import ZaimTransferRow


class WaonAutoChargeRow(WaonRow):
    """
    This class implements auto charge row model of WAON.
    """
    def convert_to_zaim_row(self) -> ZaimTransferRow:
        return ZaimTransferRow(self)
