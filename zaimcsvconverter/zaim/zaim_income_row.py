#!/usr/bin/env python
from typing import NoReturn

from zaimcsvconverter import CONFIG
from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimIncomeRow(ZaimRow):
    METHOD = 'income'

    def __init__(self, account_row):
        super().__init__(account_row, self.METHOD)

    def _initialize_by_waon_row(self, waon_row: WaonRow) -> NoReturn:
        self._category_large = ''
        self._category_small = ''
        self._cash_flow_source = '-'
        self._cash_flow_target = CONFIG.account_name_waon
        self._store = ''
        self._amount_income = waon_row.used_amount()
        self._amount_payment = 0
        self._amount_transfer = 0
        super()._initialize_by_waon_row_common(waon_row)
