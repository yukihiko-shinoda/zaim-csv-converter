#!/usr/bin/env python
from zaimcsvconverter import CONFIG
from zaimcsvconverter.mufg.mufg_abstract_income_row import MufgAbstractIncomeRow
from zaimcsvconverter.zaim.zaim_transfer_row import ZaimTransferRow


class MufgIncomeRow(MufgAbstractIncomeRow):
    def convert_to_zaim_row(self):
        return ZaimTransferRow(self)

    @property
    def cash_flow_source_on_zaim(self) -> str:
        return CONFIG.mufg.transfer_account_name
