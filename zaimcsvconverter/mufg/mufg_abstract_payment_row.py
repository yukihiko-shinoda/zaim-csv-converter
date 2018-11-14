#!/usr/bin/env python
from abc import abstractmethod

from zaimcsvconverter import CONFIG
from zaimcsvconverter.mufg.mufg_row import MufgRow


class MufgAbstractPaymentRow(MufgRow):
    @abstractmethod
    def convert_to_zaim_row(self):
        pass

    @property
    def cash_flow_source_on_zaim(self) -> str:
        return CONFIG.mufg.account_name

    @property
    @abstractmethod
    def cash_flow_target_on_zaim(self) -> str:
        pass

    @property
    def amount(self) -> int:
        return self._payed_amount
