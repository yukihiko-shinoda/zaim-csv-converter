#!/usr/bin/env python
from typing import NoReturn

from sqlalchemy.orm.exc import NoResultFound

from zaimcsvconverter.session_manager import SessionManager
from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimTransferRow(ZaimRow):
    METHOD = 'transfer'

    def get_method(self):
        return self.METHOD

    def _initialize_by_waon_row(self, waon_row: WaonRow, session_manager: SessionManager) -> NoReturn:
        from zaimcsvconverter.waon_csv_converter import WaonCsvConverter
        try:
            convert_waon_zaim_row = session_manager.find_waon_store(waon_row.use_store)
        except NoResultFound as e:
            raise KeyError(
                f'"{waon_row.use_store}" is not defined on {WaonCsvConverter.CSV_FILE_CONVERT_WAON_ZAIM}. '
                + 'Please define it.'
            ) from e
        self._category_large = ''
        self._category_small = ''
        self._cash_flow_source = ZaimRow.ACCOUNT_AEON_BANK
        self._cash_flow_target = ZaimRow.ACCOUNT_WAON
        self._store = convert_waon_zaim_row.name_zaim
        self._amount_income = 0
        self._amount_payment = 0
        self._amount_transfer = waon_row.use_amount
        super()._initialize_by_waon_row_common(waon_row)
