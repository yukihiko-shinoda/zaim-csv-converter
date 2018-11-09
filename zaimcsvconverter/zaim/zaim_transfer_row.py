#!/usr/bin/env python
from typing import NoReturn

from zaimcsvconverter import CONFIG
from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimTransferRow(ZaimRow):
    METHOD = 'transfer'

    def __init__(self, account_row):
        super().__init__(account_row, self.METHOD)

    def _initialize_by_waon_row(self, waon_row: WaonRow) -> NoReturn:
        store = self._try_to_find_waon_store(waon_row)
        self._category_large = ''
        self._category_small = ''
        self._cash_flow_source = CONFIG.waon.auto_charge_source
        self._cash_flow_target = CONFIG.waon.account_name
        self._store = store.name_zaim
        self._amount_income = 0
        self._amount_payment = 0
        self._amount_transfer = waon_row.used_amount
        super()._initialize_by_waon_row_common(
            waon_row
        )
