#!/usr/bin/env python
from zaimcsvconverter.mufg.mufg_abstract_income_row import MufgAbstractIncomeRow
from zaimcsvconverter.zaim.zaim_income_row import ZaimIncomeRow
from zaimcsvconverter.zaim.zaim_transfer_row import ZaimTransferRow


class MufgTransferIncomeRow(MufgAbstractIncomeRow):
    def convert_to_zaim_row(self):
        if self.summary_content.transfer_target is None:
            return ZaimIncomeRow(self)
        return ZaimTransferRow(self)

    @property
    def cash_flow_source_on_zaim(self) -> str:
        return self.summary_content.transfer_target
