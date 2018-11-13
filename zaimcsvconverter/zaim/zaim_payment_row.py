#!/usr/bin/env python
from typing import NoReturn, List, TYPE_CHECKING

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_row import AccountRow
from zaimcsvconverter.mufg.mufg_row import MufgRow
from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim.zaim_row import ZaimRow
if TYPE_CHECKING:
    from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_row import GoldPointCardPlusRow


class ZaimPaymentRow(ZaimRow):
    METHOD: str = 'payment'

    def __init__(self, account_row: AccountRow):
        super().__init__(account_row, self.METHOD)

    def _initialize_by_waon_row(self, waon_row: WaonRow) -> NoReturn:
        self._cash_flow_source: str = CONFIG.waon.account_name
        self._amount_payment: int = waon_row.used_amount
        super()._initialize_by_waon_row(waon_row)

    def _initialize_by_gold_point_card_plus_row(self, gold_point_card_plus_row: 'GoldPointCardPlusRow') -> NoReturn:
        self._cash_flow_source: str = CONFIG.gold_point_card_plus.account_name
        self._amount_payment: int = gold_point_card_plus_row.used_amount
        super()._initialize_by_gold_point_card_plus_row(gold_point_card_plus_row)

    def _initialize_by_mufg_row(self, mufg_row: MufgRow) -> NoReturn:
        self._cash_flow_source: str = mufg_row.cash_flow_source_on_zaim
        self._amount_payment: int = mufg_row.amount
        super()._initialize_by_mufg_row(mufg_row)

    def convert_to_list(self) -> List[str]:
        return [
            self._date.strftime("%Y-%m-%d"),
            self.METHOD,
            self._store.category_payment_large,
            self._store.category_payment_small,
            self._cash_flow_source,
            self.CASH_FLOW_TARGET_EMPTY,
            self.ITEM_NAME_EMPTY,
            self.NOTE_NAME_EMPTY,
            self._store.name_zaim,
            self.CURRENCY_EMPTY,
            self.AMOUNT_INCOME_EMPTY,
            self._amount_payment,
            self.AMOUNT_TRANSFER_EMPTY,
            self.BALANCE_ADJUSTMENT_EMPTY,
            self.AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY,
            self.SETTING_AGGREGATE_EMPTY
        ]
