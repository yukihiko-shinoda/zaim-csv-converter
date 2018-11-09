#!/usr/bin/env python
from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_payment_row import ZaimPaymentRow


class WaonPaymentRow(WaonRow):
    USE_KIND = '支払'

    def convert_to_zaim_row(self):
        return ZaimPaymentRow(self)
