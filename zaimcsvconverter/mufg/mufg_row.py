#!/usr/bin/env python

"""
This module implements row model of MUFG bank CSV.
"""

from abc import abstractmethod
import datetime
from enum import Enum
from typing import Union

from zaimcsvconverter.account_row import AccountRow
from zaimcsvconverter.enum import Account
from zaimcsvconverter.models import Store


class CashFlowKind(Enum):
    """
    This class implements constant of cash flow kind in MUFG CSV.
    """
    INCOME: str = '入金'
    PAYMENT: str = '支払い'
    TRANSFER_INCOME: str = '振替入金'
    TRANSFER_PAYMENT: str = '振替支払い'


class Index(Enum):
    """
    This class implements constant of row index in MUFG CSV.
    """
    DATE: int = 0
    SUMMARY: int = 1
    SUMMARY_CONTENT: int = 2
    PAYED_AMOUNT: int = 3
    DEPOSIT_AMOUNT: int = 4
    BALANCE: int = 5
    NOTE: int = 6
    IS_UNCAPITALIZED: int = 7
    CASH_FLOW_KIND: int = 8


# pylint: disable=too-many-instance-attributes
class MufgRow(AccountRow):
    """
    This class implements row model of MUFG bank CSV.
    """
    def __init__(self, list_row_waon):
        self._date: datetime = datetime.datetime.strptime(list_row_waon[Index.DATE.value], "%Y/%m/%d")
        self._summary: str = list_row_waon[Index.SUMMARY.value]
        self._summary_content: Store = Store.try_to_find(Account.MUFG, list_row_waon[Index.SUMMARY_CONTENT.value])
        self._payed_amount: int = self._convert_string_to_int_or_none(list_row_waon[Index.PAYED_AMOUNT.value])
        self._deposit_amount: int = self._convert_string_to_int_or_none(list_row_waon[Index.DEPOSIT_AMOUNT.value])
        self._balance = int(list_row_waon[Index.BALANCE.value].replace(',', ''))
        self._note: str = list_row_waon[Index.NOTE.value]
        self._is_uncapitalized: str = list_row_waon[Index.IS_UNCAPITALIZED.value]

    @staticmethod
    def _convert_string_to_int_or_none(string) -> Union[int, None]:
        if string == '':
            return None
        return int(string.replace(',', ''))

    @property
    @abstractmethod
    def _cash_flow_source_on_zaim(self) -> str:
        pass

    @property
    @abstractmethod
    def _cash_flow_target_on_zaim(self) -> str:
        pass

    @property
    @abstractmethod
    def _amount(self) -> int:
        pass

    @property
    def zaim_date(self) -> datetime:
        return self._date

    @property
    def zaim_store(self) -> Store:
        return self._summary_content

    @property
    def zaim_income_cash_flow_target(self) -> str:
        return self._cash_flow_target_on_zaim

    @property
    def zaim_income_ammount_income(self) -> int:
        return self._amount

    @property
    def zaim_payment_cash_flow_source(self) -> str:
        return self._cash_flow_source_on_zaim

    @property
    def zaim_payment_amount_payment(self) -> int:
        return self._amount

    @property
    def zaim_transfer_cash_flow_source(self) -> str:
        return self._cash_flow_source_on_zaim

    @property
    def zaim_transfer_cash_flow_target(self) -> str:
        return self._cash_flow_target_on_zaim

    @property
    def zaim_transfer_amount_transfer(self) -> int:
        return self._amount
