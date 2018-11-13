#!/usr/bin/env python
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zaimcsvconverter.zaim.zaim_row import ZaimRow


class AccountRow(metaclass=ABCMeta):
    @abstractmethod
    def convert_to_zaim_row(self) -> 'ZaimRow':
        pass
