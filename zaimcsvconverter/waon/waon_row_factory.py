#!/usr/bin/env python
from zaimcsvconverter.waon.waon_auto_charge_row import WaonAutoChargeRow
from zaimcsvconverter.waon.waon_payment_row import WaonPaymentRow
from zaimcsvconverter.waon.waon_row import WaonRow


class WaonRowFactory(object):
    @staticmethod
    def create(list_row_waon):
        use_kind = list_row_waon[WaonRow.INDEX_USE_KIND]
        waon_row = {
            WaonPaymentRow.USE_KIND: WaonPaymentRow(list_row_waon),
            WaonAutoChargeRow.USE_KIND: WaonAutoChargeRow(list_row_waon)
        }.get(use_kind)

        if waon_row is None:
            raise NotImplementedError(
                'The value of "Use kind" has not been defined in this code. Use kind =' + use_kind
            )

        return waon_row

