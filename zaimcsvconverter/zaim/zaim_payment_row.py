#!/usr/bin/env python
from typing import NoReturn

from zaimcsvconverter import CONFIG
from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimPaymentRow(ZaimRow):
    METHOD = 'payment'

    def __init__(self, account_row):
        super().__init__(account_row, self.METHOD)

    def _initialize_by_waon_row(self, waon_row: WaonRow) -> NoReturn:
        store = self._try_to_find_waon_store(waon_row)
        self._category_large = store.category_large
        self._category_small = store.category_small
        self._cash_flow_source = CONFIG.waon.account_name
        self._cash_flow_target = '-'
        self._store = store.name_zaim
        self._amount_income = 0
        self._amount_payment = waon_row.used_amount
        self._amount_transfer = 0
        super()._initialize_by_waon_row_common(waon_row)
