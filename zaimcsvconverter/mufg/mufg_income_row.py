#!/usr/bin/env python
from zaimcsvconverter import CONFIG
from zaimcsvconverter.mufg.mufg_row import MufgRow
from zaimcsvconverter.zaim.zaim_transfer_row import ZaimTransferRow


class MufgIncomeRow(MufgRow):
    def convert_to_zaim_row(self):
        return ZaimTransferRow(self)

    @property
    def cash_flow_source_on_zaim(self) -> str:
        return CONFIG.mufg.transfer_account_name

    @property
    def cash_flow_target_on_zaim(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def amount(self) -> int:
        return self._deposit_amount
