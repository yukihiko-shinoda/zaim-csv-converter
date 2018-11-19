#!/usr/bin/env python

"""
This module implements row model of CSV.
"""

from __future__ import annotations
import datetime
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, List

from zaimcsvconverter.models import Store, Item

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


class AccountStoreRowData(AccountRowData):
    """This class is abstract class of account CSV row data."""
    @property
    @abstractmethod
    def store_name(self) -> str:
        """This property returns store name."""
        pass


class AccountItemRowData(AccountRowData):
    """This class is abstract class of account CSV row data."""
    @property
    @abstractmethod
    def item_name(self) -> str:
        """This property returns store name."""
        pass


class AccountRow(metaclass=ABCMeta):
    """
    This class implements row model of CSV.
    """
    @property
    def is_valid(self) -> bool:
        """This property returns whether this row is valid or not."""
        return self.zaim_store is not None

    # pylint: disable=no-self-use
    def extract_undefined_content(self, account_row_data: AccountStoreRowData) -> List[str]:
        """This property extract undefined content from account_row_data and return it."""
        return [account_row_data.store_name, '']

    @property
    def is_row_to_skip(self) -> bool:
        """This property returns whether this row should be skipped or not."""
        return False

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
    def zaim_item(self) -> None:
        """This property return item in Zaim row."""
        return None

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
        from zaimcsvconverter.account_dependency import Account
        account_dependency = Account.create_by_account_row(self).value
        return Store.try_to_find(account_dependency, store_name)

    def try_to_find_item(self, item_name) -> Item:
        """This method select store from database and return it as Store model."""
        from zaimcsvconverter.account_dependency import Account
        account_dependency = Account.create_by_account_row(self).value
        return Item.try_to_find(account_dependency, item_name)


class AccountItemRow(AccountRow):
    """
    This class implements store row model of CSV.
    """
    @property
    def is_valid(self) -> bool:
        """This property returns whether this row is valid or not."""
        return self.zaim_store is not None and self.zaim_item is not None

    def extract_undefined_content(self, account_row_data: AccountItemRowData) -> List[str]:
        """This property extract undefined content from account_row_data and return it."""
        return [
            '',
            account_row_data.item_name
        ]

    @property
    @abstractmethod
    def zaim_item(self) -> 'Item':
        """This property return item in Zaim row."""
        pass
