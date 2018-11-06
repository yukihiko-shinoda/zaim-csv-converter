#!/usr/bin/env python
from typing import NoReturn

from zaimcsvconverter.session_manager import SessionManager
from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimIncomeRow(ZaimRow):
    METHOD = 'income'

    def get_method(self):
        return self.METHOD

    def _initialize_by_waon_row(self, waon_row: WaonRow, session_manager: SessionManager) -> NoReturn:
        self._category_large = ''
        self._category_small = ''
        self._cash_flow_source = '-'
        self._cash_flow_target = ZaimRow.ACCOUNT_WAON
        self._store = ''
        self._amount_income = waon_row.use_amount()
        self._amount_payment = 0
        self._amount_transfer = 0
        super()._initialize_by_waon_row_common(waon_row)
