#!/usr/bin/env python
from abc import abstractmethod
import datetime
from enum import Enum
from typing import Union, TYPE_CHECKING

from zaimcsvconverter.account_row import AccountRow
from zaimcsvconverter.enum import Account
from zaimcsvconverter.models import Store
if TYPE_CHECKING:
    from zaimcsvconverter.zaim.zaim_row import ZaimRow


class CashFlowKind(Enum):
    INCOME: str = '入金'
    PAYMENT: str = '支払い'
    TRANSFER_INCOME: str = '振替入金'
    TRANSFER_PAYMENT: str = '振替支払い'


class MufgRow(AccountRow):
    INDEX_DATE: int = 0
    INDEX_SUMMARY: int = 1
    INDEX_SUMMARY_CONTENT: int = 2
    INDEX_PAYED_AMOUNT: int = 3
    INDEX_DEPOSIT_AMOUNT: int = 4
    INDEX_BALANCE: int = 5
    INDEX_NOTE: int = 6
    INDEX_IS_UNCAPITALIZED: int = 7
    INDEX_CASH_FLOW_KIND: int = 8

    def __init__(self, list_row_waon):
        self._date: datetime = datetime.datetime.strptime(list_row_waon[self.INDEX_DATE], "%Y/%m/%d")
        self._summary: str = list_row_waon[self.INDEX_SUMMARY]
        self._summary_content: Store = Store.try_to_find(Account.MUFG, list_row_waon[self.INDEX_SUMMARY_CONTENT])
        self._payed_amount: int = self.convert_string_to_int_or_none(list_row_waon[self.INDEX_PAYED_AMOUNT].replace(',', ''))
        self._deposit_amount: int = self.convert_string_to_int_or_none(list_row_waon[self.INDEX_DEPOSIT_AMOUNT].replace(',', ''))
        self._balance = int(list_row_waon[self.INDEX_BALANCE].replace(',', ''))
        self._note: str = list_row_waon[self.INDEX_NOTE]
        self._is_uncapitalized: str = list_row_waon[self.INDEX_IS_UNCAPITALIZED]

    @staticmethod
    def convert_string_to_int_or_none(string) -> Union[int, None]:
        if string is '':
            return None
        else:
            return int(string)

    @abstractmethod
    def convert_to_zaim_row(self) -> 'ZaimRow':
        pass

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def summary_content(self) -> Store:
        return self._summary_content

    @property
    @abstractmethod
    def cash_flow_source_on_zaim(self) -> str:
        pass

    @property
    @abstractmethod
    def cash_flow_target_on_zaim(self) -> str:
        pass

    @property
    @abstractmethod
    def amount(self) -> int:
        pass
