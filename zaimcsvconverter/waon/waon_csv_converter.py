#!/usr/bin/env python
from zaimcsvconverter.AccountCsvConverter import AccountCsvConverter
from zaimcsvconverter.waon.waon_auto_charge_row import WaonAutoChargeRow
from zaimcsvconverter.waon.waon_payment_row import WaonPaymentRow
from zaimcsvconverter.waon.waon_row import WaonRow


class WaonCsvConverter(AccountCsvConverter):
    def __init__(self, csv_file):
        super().__init__(csv_file, 'UTF-8', True)

    def _create_account_row(self, list_row_account):
        use_kind = list_row_account[WaonRow.INDEX_USED_KIND]
        waon_row = {
            WaonPaymentRow.USE_KIND: WaonPaymentRow(list_row_account),
            WaonAutoChargeRow.USE_KIND: WaonAutoChargeRow(list_row_account)
        }.get(use_kind)

        if waon_row is None:
            raise NotImplementedError(
                'The value of "Use kind" has not been defined in this code. Use kind =' + use_kind
            )

        return waon_row
