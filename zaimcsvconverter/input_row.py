"""This module implements row model of CSV."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Optional, TypeVar, Generic, Type

from zaimcsvconverter.exceptions import InvalidRowError, RowToSkip
from zaimcsvconverter.models import Store, Item

if TYPE_CHECKING:
    from zaimcsvconverter.account import Account
    from zaimcsvconverter.zaim_row import ZaimRow


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


TypeVarInputRowData = TypeVar('TypeVarInputRowData', bound=InputRowData)


class InputRowFactory(Generic[TypeVarInputRowData]):
    """This class implements factory to create input CSV row instance."""
    @abstractmethod
    def create(self, account: 'Account', row_data: TypeVarInputRowData) -> InputRow:
        """This method creates input row by input CSV row data."""


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

    @abstractmethod
    def validate(self) -> ValidatedInputRow:
        """This property returns whether this row is valid or not."""

    # pylint: disable=unused-argument,no-self-use
    def is_row_to_skip(self, store: Store) -> bool:
        """This property returns whether this row should be skipped or not."""
        return False

    def try_to_convert_to_zaim_row(self) -> 'ZaimRow':
        """This function try to convert this row to Zaim row."""
        validated_input_row = self.validate()
        if validated_input_row.is_row_to_skip:
            raise RowToSkip()
        zaim_row_class = validated_input_row.zaim_row_class_to_convert()
        return zaim_row_class(validated_input_row)

    @abstractmethod
    def zaim_row_class_to_convert(self, store: Store) -> Type['ZaimRow']:
        """This method converts this row to row of Zaim."""

    @property
    @abstractmethod
    def zaim_store(self) -> Optional['Store']:
        """This property return store in Zaim row."""

    @property
    @abstractmethod
    def zaim_item(self) -> Optional['Item']:
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

    def try_to_find_store(self, store_name) -> Optional[Store]:
        """This method select store from database and return it as Store model."""
        return Store.try_to_find(self._account, store_name)

    def try_to_find_item(self, item_name) -> Optional[Item]:
        """This method select store from database and return it as Store model."""
        return Item.try_to_find(self._account, item_name)


class InputStoreRow(InputRow):
    """This class implements store row model of CSV."""
    def __init__(self, account: 'Account', input_store_row_data: InputStoreRowData):
        super().__init__(account, input_store_row_data)
        self._account = account
        self._zaim_store = self.try_to_find_store(input_store_row_data.store_name)

    def validate(self) -> ValidatedInputStoreRow:
        """This property returns whether this row is valid or not."""
        if self.zaim_store is None:
            raise InvalidRowError()
        return ValidatedInputStoreRow(self, self.zaim_store)

    @property
    def zaim_store(self) -> Optional[Store]:
        return self._zaim_store

    @property
    def zaim_item(self) -> None:
        return None

    @abstractmethod
    def zaim_row_class_to_convert(self, store: Store) -> Type['ZaimRow']:
        pass


class InputItemRow(InputRow):
    """This class implements store row model of CSV."""
    def __init__(self, account: 'Account', input_item_row_data: InputItemRowData):
        super().__init__(account, input_item_row_data)
        self._account = account
        self._zaim_item = self.try_to_find_item(input_item_row_data.item_name)

    def validate(self) -> ValidatedInputItemRow:
        """This property returns whether this row is valid or not."""
        if self.zaim_store is None or self.zaim_item is None:
            raise InvalidRowError()
        return ValidatedInputItemRow(self, self.zaim_store, self.zaim_item)

    @property
    @abstractmethod
    def zaim_store(self) -> Store:
        pass

    @property
    def zaim_item(self) -> Optional[Item]:
        return None


class ValidatedInputRow:
    """This class implements validated row model of CSV."""
    input_row: InputRow
    zaim_store: Store

    @property
    @abstractmethod
    def is_row_to_skip(self) -> bool:
        """This property returns whether this row should be skipped or not."""

    def zaim_row_class_to_convert(self):
        """This method converts this row to row of Zaim."""
        return self.input_row.zaim_row_class_to_convert(self.zaim_store)


@dataclass
class ValidatedInputStoreRow(ValidatedInputRow):
    """This class implements validated store row model of CSV."""
    input_row: InputRow
    zaim_store: Store

    @property
    def is_row_to_skip(self) -> bool:
        """This property returns whether this row should be skipped or not."""
        return self.input_row.is_row_to_skip(self.zaim_store)


@dataclass
class ValidatedInputItemRow(ValidatedInputRow):
    """This class implements validated item row model of CSV."""
    input_row: InputRow
    zaim_store: Store
    zaim_item: Item

    @property
    def is_row_to_skip(self) -> bool:
        return False
