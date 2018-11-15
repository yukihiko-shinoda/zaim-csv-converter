#!/usr/bin/env python

"""
This module implements row model of WAON CSV.
"""

from abc import abstractmethod
import datetime
import re
from enum import Enum
from typing import List, TYPE_CHECKING

from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_row import AccountRow
from zaimcsvconverter.enum import Account
from zaimcsvconverter.models import Store
if TYPE_CHECKING:
    from zaimcsvconverter.zaim.zaim_row import ZaimRow


class WaonRow(AccountRow):
    """
    This class implements row model of WAON CSV.
    """
    class UseKind(Enum):
        """
        This class implements constant of user kind in WAON CSV.
        """
        PAYMENT: str = '支払'
        AUTO_CHARGE: str = 'オートチャージ'

    INDEX_DATE: int = 0
    INDEX_USED_STORE: int = 1
    INDEX_USED_AMOUNT: int = 2
    INDEX_USED_KIND: int = 3
    INDEX_CHARGE_KIND: int = 4

    def __init__(self, list_row_waon: List[str]):
        self._date: datetime = datetime.datetime.strptime(list_row_waon[self.INDEX_DATE], "%Y/%m/%d")
        self._used_store: Store = Store.try_to_find(Account.WAON, list_row_waon[self.INDEX_USED_STORE])
        used_amount = re.search(r'([\d,]+)円', list_row_waon[self.INDEX_USED_AMOUNT])
        self._used_amount: int = int(used_amount.group(1).replace(',', ''))
        self._charge_kind: str = list_row_waon[self.INDEX_CHARGE_KIND]

    @abstractmethod
    def convert_to_zaim_row(self) -> 'ZaimRow':
        pass

    @property
    def zaim_date(self) -> datetime:
        return self._date

    @property
    def zaim_store(self) -> Store:
        return self._used_store

    @property
    def zaim_income_cash_flow_target(self) -> str:
        return CONFIG.waon.account_name

    @property
    def zaim_income_ammount_income(self) -> int:
        return self._used_amount

    @property
    def zaim_payment_cash_flow_source(self) -> str:
        return CONFIG.waon.account_name

    @property
    def zaim_payment_amount_payment(self) -> int:
        return self._used_amount

    @property
    def zaim_transfer_cash_flow_source(self) -> str:
        return CONFIG.waon.auto_charge_source

    @property
    def zaim_transfer_cash_flow_target(self) -> str:
        return CONFIG.waon.account_name

    @property
    def zaim_transfer_amount_transfer(self) -> int:
        return self._used_amount
