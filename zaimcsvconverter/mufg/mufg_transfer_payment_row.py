#!/usr/bin/env python
from zaimcsvconverter import CONFIG
from zaimcsvconverter.mufg.mufg_row import MufgRow
from zaimcsvconverter.zaim.zaim_payment_row import ZaimPaymentRow
from zaimcsvconverter.zaim.zaim_transfer_row import ZaimTransferRow


class MufgTransferPaymentRow(MufgRow):
    def convert_to_zaim_row(self):
        if self.summary_content.transfer_target is None:
            return ZaimPaymentRow(self)
        else:
            return ZaimTransferRow(self)

    @property
    def cash_flow_source_on_zaim(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def cash_flow_target_on_zaim(self) -> str:
        return self.summary_content.transfer_target

    @property
    def amount(self) -> int:
        return self._payed_amount
