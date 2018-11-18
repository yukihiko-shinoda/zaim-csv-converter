#!/usr/bin/env python

"""
This module implements row model of CSV.
"""

from __future__ import annotations
import datetime
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from zaimcsvconverter.models import Store

if TYPE_CHECKING:
    from zaimcsvconverter.zaim_row import ZaimRow


class AccountRowData(metaclass=ABCMeta):
    """This class is abstract class of account CSV row data."""
    def __init__(self, *args):
        pass

    @property
    @abstractmethod
    def date(self) -> datetime:
        """This property returns date as datetime."""
        pass

    @property
    @abstractmethod
    def store_name(self) -> str:
        """This property returns store name."""
        pass


class AccountRow(metaclass=ABCMeta):
    """
    This class implements row model of CSV.
    """
    @abstractmethod
    def convert_to_zaim_row(self) -> 'ZaimRow':
        """
        This method converts this row to row of Zaim.
        """
        pass

    @property
    @abstractmethod
    def zaim_date(self) -> datetime:
        """
        This property return date in Zaim row.
        """
        pass

    @property
    @abstractmethod
    def zaim_store(self) -> 'Store':
        """
        This property return store in Zaim row.
        """
        pass

    @property
    @abstractmethod
    def zaim_income_cash_flow_target(self) -> str:
        """
        This property return cash flow target in Zaim income row.
        """
        pass

    @property
    @abstractmethod
    def zaim_income_ammount_income(self) -> int:
        """
        This property return amount of income in Zaim income row.
        """
        pass

    @property
    @abstractmethod
    def zaim_payment_cash_flow_source(self) -> str:
        """
        This property return cash flow source in Zaim payment row.
        """
        pass

    @property
    @abstractmethod
    def zaim_payment_amount_payment(self) -> int:
        """
        This property return amount of payment in Zaim payment row.
        """
        pass

    @property
    @abstractmethod
    def zaim_transfer_cash_flow_source(self) -> str:
        """
        This property return cash flow source in Zaim transfer row.
        """
        pass

    @property
    @abstractmethod
    def zaim_transfer_cash_flow_target(self) -> str:
        """
        This property return cash flow target in Zaim transfer row.
        """
        pass

    @property
    @abstractmethod
    def zaim_transfer_amount_transfer(self) -> int:
        """
        This property return amount of transfer in Zaim transfer row.
        """
        pass


    @staticmethod
    @abstractmethod
    def create(row_data: AccountRowData) -> AccountRow:
        """This method creates account row by account row data."""
        pass

    def try_to_find_store(self, store_name) -> Store:
        """This method select store from database and return it as Store model."""
        from zaimcsvconverter.enum import Account
        account_dependency = Account.create_by_account_row(self).value
        return Store.try_to_find(account_dependency, store_name)
