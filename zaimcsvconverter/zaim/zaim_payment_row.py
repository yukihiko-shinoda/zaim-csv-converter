#!/usr/bin/env python
from typing import NoReturn

from zaimcsvconverter.database_wrapper import DatabaseWrapper
from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimPaymentRow(ZaimRow):
    METHOD = 'payment'

    def get_method(self):
        return self.METHOD

    def _initialize_by_waon_row(self, waon_row: WaonRow, database_wrapper: DatabaseWrapper) -> NoReturn:
        from zaimcsvconverter.waon_csv_converter import WaonCsvConverter
        convert_waon_zaim_row = database_wrapper.find_convert_waon_zaim(waon_row.use_store)
        if convert_waon_zaim_row is None:
            # TODO 0件だった場合例外となることをunittest
            raise KeyError(
                f'"{waon_row.use_store}" is not defined on {WaonCsvConverter.CSV_FILE_CONVERT_WAON_ZAIM}. '
                + 'Please define it.'
            )
        self._category_large = convert_waon_zaim_row.category_large
        self._category_small = convert_waon_zaim_row.category_small
        self._cash_flow_source = ZaimRow.ACCOUNT_WAON
        self._cash_flow_target = '-'
        self._store = convert_waon_zaim_row.store_zaim
        self._amount_income = 0
        self._amount_payment = waon_row.use_amount
        self._amount_transfer = 0
        super()._initialize_by_waon_row_common(waon_row)
