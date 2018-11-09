#!/usr/bin/env python
from abc import ABCMeta, abstractmethod


class AccountRow(metaclass=ABCMeta):
    @abstractmethod
    def convert_to_zaim_row(self):
        pass
