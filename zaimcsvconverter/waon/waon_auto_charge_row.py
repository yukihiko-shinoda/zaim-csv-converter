#!/usr/bin/env python
from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_transfer_row import ZaimTransferRow


class WaonAutoChargeRow(WaonRow):
    def convert_to_zaim_row(self) -> ZaimTransferRow:
        return ZaimTransferRow(self)
