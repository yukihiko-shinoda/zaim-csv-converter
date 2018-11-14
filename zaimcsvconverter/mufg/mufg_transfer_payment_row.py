#!/usr/bin/env python
from zaimcsvconverter.mufg.mufg_abstract_payment_row import MufgAbstractPaymentRow
from zaimcsvconverter.zaim.zaim_payment_row import ZaimPaymentRow
from zaimcsvconverter.zaim.zaim_transfer_row import ZaimTransferRow


class MufgTransferPaymentRow(MufgAbstractPaymentRow):
    def convert_to_zaim_row(self):
        if self.summary_content.transfer_target is None:
            return ZaimPaymentRow(self)
        return ZaimTransferRow(self)

    @property
    def cash_flow_target_on_zaim(self) -> str:
        return self.summary_content.transfer_target
