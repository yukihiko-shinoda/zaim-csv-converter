#!/usr/bin/env python
from zaimcsvconverter import CONFIG
from zaimcsvconverter.mufg.mufg_abstract_payment_row import MufgAbstractPaymentRow
from zaimcsvconverter.zaim.zaim_transfer_row import ZaimTransferRow


class MufgPaymentRow(MufgAbstractPaymentRow):
    def convert_to_zaim_row(self):
        return ZaimTransferRow(self)

    @property
    def cash_flow_target_on_zaim(self) -> str:
        return CONFIG.mufg.transfer_account_name
