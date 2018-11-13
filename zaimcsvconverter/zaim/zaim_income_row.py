#!/usr/bin/env python
from typing import NoReturn, List

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_row import AccountRow
from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_row import GoldPointCardPlusRow
from zaimcsvconverter.mufg.mufg_row import MufgRow
from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_row import ZaimRow


class ZaimIncomeRow(ZaimRow):
    METHOD: str = 'income'

    def __init__(self, account_row: AccountRow):
        super().__init__(account_row, self.METHOD)

    def _initialize_by_waon_row(self, waon_row: WaonRow) -> NoReturn:
        self._cash_flow_target: str = CONFIG.waon.account_name
        self._amount_income: int = waon_row.used_amount
        super()._initialize_by_waon_row(waon_row)

    def _initialize_by_gold_point_card_plus_row(self, gold_point_card_plus_row: GoldPointCardPlusRow) -> NoReturn:
        raise ValueError('Income row for GOLD POINT CARD+ is not defined. Please confirm CSV file.')

    def _initialize_by_mufg_row(self, mufg_row: MufgRow) -> NoReturn:
        self._cash_flow_target: str = mufg_row.cash_flow_target_on_zaim
        self._amount_income: int = mufg_row.amount
        super()._initialize_by_mufg_row(mufg_row)

    def convert_to_list(self) -> List[str]:
        return [
            self._date.strftime("%Y-%m-%d"),
            self.METHOD,
            self._store.category_income,
            self.CATEGORY_SMALL_EMPTY,
            self.CASH_FLOW_SOURCE_EMPTY,
            self._cash_flow_target,
            self.ITEM_NAME_EMPTY,
            self.NOTE_NAME_EMPTY,
            self._store.name_zaim,
            self.CURRENCY_EMPTY,
            self._amount_income,
            self.AMOUNT_PAYMENT_EMPTY,
            self.AMOUNT_TRANSFER_EMPTY,
            self.BALANCE_ADJUSTMENT_EMPTY,
            self.AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY,
            self.SETTING_AGGREGATE_EMPTY
        ]
