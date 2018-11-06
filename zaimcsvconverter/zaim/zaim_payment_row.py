#!/usr/bin/env python
from typing import NoReturn

from sqlalchemy.orm.exc import NoResultFound

from zaimcsvconverter.session_manager import SessionManager
from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimPaymentRow(ZaimRow):
    METHOD = 'payment'

    def get_method(self):
        return self.METHOD

    def _initialize_by_waon_row(self, waon_row: WaonRow, session_manager: SessionManager) -> NoReturn:
        from zaimcsvconverter.waon_csv_converter import WaonCsvConverter
        try:
            waon_store = session_manager.find_waon_store(waon_row.use_store)
        except NoResultFound as e:
            raise KeyError(
                f'"{waon_row.use_store}" is not defined on {WaonCsvConverter.CSV_FILE_CONVERT_WAON_ZAIM}. '
                + 'Please define it.'
            ) from e
        self._category_large = waon_store.category_large
        self._category_small = waon_store.category_small
        self._cash_flow_source = ZaimRow.ACCOUNT_WAON
        self._cash_flow_target = '-'
        self._store = waon_store.name_zaim
        self._amount_income = 0
        self._amount_payment = waon_row.use_amount
        self._amount_transfer = 0
        super()._initialize_by_waon_row_common(waon_row)
