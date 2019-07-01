#!/usr/bin/env python

"""
This module implements row model of CSV.
"""

from __future__ import annotations
import datetime
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from zaimcsvconverter.models import Store, Item

if TYPE_CHECKING:
    from zaimcsvconverter.account import Account
    from zaimcsvconverter.zaim_row import ZaimRow


class InputRowFactory(metaclass=ABCMeta):
    """This class implements factory to create input CSV row instance."""
    @abstractmethod
    def create(self, account: 'Account', row_data: InputRowData) -> InputRow:
        """This method creates input row by input CSV row data."""


class InputRowData(metaclass=ABCMeta):
    """This class is abstract class of input CSV row data."""
    def __init__(self, *args):
        pass

    @property
    @abstractmethod
    def date(self) -> datetime:
        """This property returns date as datetime."""

    @property
    @abstractmethod
    def store_name(self) -> str:
        """This property returns store name."""

    @property
    @abstractmethod
    def item_name(self) -> str:
        """This property returns store name."""


class InputStoreRowData(InputRowData):
    """This class is abstract class of input CSV row data."""
    @property
    @abstractmethod
    def store_name(self) -> str:
        pass

    @property
    def item_name(self) -> str:
        return ''


class InputItemRowData(InputRowData):
    """This class is abstract class of input CSV row data."""
    @property
    def store_name(self) -> str:
        return ''

    @property
    @abstractmethod
    def item_name(self) -> str:
        pass


class InputRow:
    """This class implements row model of CSV."""
    def __init__(self, account: 'Account', input_row_data: InputRowData):
        self._account = account
        self.zaim_date = input_row_data.date

    @property
    def is_valid(self) -> bool:
        """This property returns whether this row is valid or not."""
        return self.zaim_store is not None

    @property
    def is_row_to_skip(self) -> bool:
        """This property returns whether this row should be skipped or not."""
        return False

    @abstractmethod
    def convert_to_zaim_row(self) -> 'ZaimRow':
        """This method converts this row to row of Zaim."""

    @property
    @abstractmethod
    def zaim_store(self) -> 'Store':
        """This property return store in Zaim row."""

    @property
    @abstractmethod
    def zaim_item(self) -> 'Item':
        """This property return item in Zaim row."""

    @property
    @abstractmethod
    def zaim_income_cash_flow_target(self) -> str:
        """This property return cash flow target in Zaim income row."""

    @property
    @abstractmethod
    def zaim_income_ammount_income(self) -> int:
        """This property return amount of income in Zaim income row."""

    @property
    @abstractmethod
    def zaim_payment_cash_flow_source(self) -> str:
        """This property return cash flow source in Zaim payment row."""

    @property
    def zaim_payment_note(self) -> str:
        """This property return cash flow source in Zaim payment row."""
        from zaimcsvconverter.zaim_row import ZaimRow
        return ZaimRow.NOTE_EMPTY

    @property
    @abstractmethod
    def zaim_payment_amount_payment(self) -> int:
        """This property return amount of payment in Zaim payment row."""

    @property
    @abstractmethod
    def zaim_transfer_cash_flow_source(self) -> str:
        """This property return cash flow source in Zaim transfer row."""

    @property
    @abstractmethod
    def zaim_transfer_cash_flow_target(self) -> str:
        """This property return cash flow target in Zaim transfer row."""

    @property
    @abstractmethod
    def zaim_transfer_amount_transfer(self) -> int:
        """This property return amount of transfer in Zaim transfer row."""

    def try_to_find_store(self, store_name) -> Store:
        """This method select store from database and return it as Store model."""
        return Store.try_to_find(self._account, store_name)

    def try_to_find_item(self, item_name) -> Item:
        """This method select store from database and return it as Store model."""
        return Item.try_to_find(self._account, item_name)


class InputStoreRow(InputRow, metaclass=ABCMeta):
    """This class implements store row model of CSV."""
    def __init__(self, account: 'Account', input_store_row_data: InputStoreRowData):
        super().__init__(account, input_store_row_data)
        self._account = account
        self._zaim_store = self.try_to_find_store(input_store_row_data.store_name)

    @property
    def is_valid(self) -> bool:
        """This property returns whether this row is valid or not."""
        return self.zaim_store is not None

    @property
    def zaim_store(self) -> Store:
        return self._zaim_store

    @property
    def zaim_item(self) -> None:
        return None

    @abstractmethod
    def convert_to_zaim_row(self) -> 'ZaimRow':
        pass


class InputItemRow(InputRow, metaclass=ABCMeta):
    """This class implements store row model of CSV."""
    def __init__(self, account: 'Account', input_item_row_data: InputItemRowData):
        super().__init__(account, input_item_row_data)
        self._account = account
        self._zaim_item = self.try_to_find_item(input_item_row_data.item_name)

    @property
    def is_valid(self) -> bool:
        """This property returns whether this row is valid or not."""
        return self.zaim_store is not None and self.zaim_item is not None

    @property
    @abstractmethod
    def zaim_store(self) -> Store:
        pass

    @property
    def zaim_item(self) -> None:
        return None
