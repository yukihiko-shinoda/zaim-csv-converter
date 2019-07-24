"""This module implements row model of CSV."""
from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Optional, TypeVar, Generic

from zaimcsvconverter.exceptions import InvalidRowError
from zaimcsvconverter.models import AccountId, Store, Item


class InputRowData:
    """This class is abstract class of input CSV row data."""
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
    # @see https://github.com/PyCQA/pylint/issues/179
    @property
    @abstractmethod
    def store_name(self) -> str:
        """This property returns store name."""

    @property
    def item_name(self) -> str:
        return ''


class InputItemRowData(InputRowData):
    """This class is abstract class of input CSV row data."""
    @property
    def store_name(self) -> str:
        return ''

    # @see https://github.com/PyCQA/pylint/issues/179
    @property
    @abstractmethod
    def item_name(self) -> str:
        """This property returns store name."""


TypeVarInputRowData = TypeVar('TypeVarInputRowData', bound=InputRowData)


class InputRow(Generic[TypeVarInputRowData]):
    """This class implements row model of CSV."""
    def __init__(self, account_id: AccountId, input_row_data: TypeVarInputRowData):
        self._account_id = account_id
        self.data = input_row_data
        self.zaim_date = input_row_data.date

    @abstractmethod
    def validate(self) -> ValidatedInputRow:
        """This property returns whether this row is valid or not."""

    # pylint: disable=unused-argument,no-self-use
    def is_row_to_skip(self, store: Store) -> bool:
        """This property returns whether this row should be skipped or not."""
        return False


class InputStoreRow(InputRow):
    """This class implements store row model of CSV."""
    def __init__(self, account_id: AccountId, input_store_row_data: InputStoreRowData):
        super().__init__(account_id, input_store_row_data)
        self.store = self.try_to_find_store(input_store_row_data.store_name)

    def validate(self) -> ValidatedInputStoreRow:
        """This property returns whether this row is valid or not."""
        if self.store is None:
            raise InvalidRowError(
                'Store name has not been defined in convert table CSV.'
                f'Store name = {self.data.store_name}'
            )
        return ValidatedInputStoreRow(self, self.store)

    def try_to_find_store(self, store_name) -> Optional[Store]:
        """This method select store from database and return it as Store model."""
        return Store.try_to_find(self._account_id, store_name)


class InputItemRow(InputRow):
    """This class implements store row model of CSV."""
    def __init__(self, account_id: AccountId, input_item_row_data: InputItemRowData):
        super().__init__(account_id, input_item_row_data)
        self.item = self.try_to_find_item(input_item_row_data.item_name)

    def validate(self) -> ValidatedInputItemRow:
        """This property returns whether this row is valid or not."""
        if self.store is None or self.item is None:
            raise InvalidRowError(
                'Store name has not been defined in convert table CSV.'
                f'Store name = {self.data.store_name}'
            )
        return ValidatedInputItemRow(self, self.store, self.item)

    @property
    @abstractmethod
    def store(self) -> Store:
        """This property returns store in Zaim row."""

    def try_to_find_item(self, item_name) -> Optional[Item]:
        """This method select store from database and return it as Store model."""
        return Item.try_to_find(self._account_id, item_name)


TypeVarInputRow = TypeVar('TypeVarInputRow', bound=InputRow)


class InputRowFactory(Generic[TypeVarInputRowData, TypeVarInputRow]):
    """This class implements factory to create input CSV row instance."""
    @abstractmethod
    def create(self, account_id: AccountId, row_data: TypeVarInputRowData) -> TypeVarInputRow:
        """This method creates input row by input CSV row data."""


class ValidatedInputRow(Generic[TypeVarInputRow]):
    """This class implements validated row model of CSV."""
    def __init__(self, input_row: TypeVarInputRow, store: Store):
        self.input_row = input_row
        self.store = store

    @property
    @abstractmethod
    def is_row_to_skip(self) -> bool:
        """This property returns whether this row should be skipped or not."""


class ValidatedInputStoreRow(ValidatedInputRow):
    """This class implements validated store row model of CSV."""
    @property
    def is_row_to_skip(self) -> bool:
        """This property returns whether this row should be skipped or not."""
        return self.input_row.is_row_to_skip(self.store)


class ValidatedInputItemRow(ValidatedInputRow):
    """This class implements validated item row model of CSV."""
    def __init__(self, input_row: InputRow, store: Store, item: Item):
        self.item = item
        super().__init__(input_row, store)

    @property
    def is_row_to_skip(self) -> bool:
        return False
