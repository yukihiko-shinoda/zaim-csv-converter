#!/usr/bin/env python
from pathlib import Path
from typing import List

from zaimcsvconverter.account_csv_converter import AccountCsvConverter
from zaimcsvconverter.waon.waon_auto_charge_row import WaonAutoChargeRow
from zaimcsvconverter.waon.waon_payment_row import WaonPaymentRow
from zaimcsvconverter.waon.waon_row import WaonRow


class WaonCsvConverter(AccountCsvConverter):
    def __init__(self, csv_file: Path):
        super().__init__(csv_file, 'UTF-8', True)

    @staticmethod
    def _create_account_row(list_row_account: List[str]) -> WaonRow:
        use_kind = list_row_account[WaonRow.INDEX_USED_KIND]
        try:
            use_kind = WaonRow.UseKind(use_kind)
        except ValueError as error:
            raise NotImplementedError(
                'The value of "Use kind" has not been defined in this code. Use kind =' + use_kind
            ) from error

        return {
            WaonRow.UseKind.PAYMENT: WaonPaymentRow(list_row_account),
            WaonRow.UseKind.AUTO_CHARGE: WaonAutoChargeRow(list_row_account)
        }.get(use_kind)
