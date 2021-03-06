"""This module implements row model of CSV."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Generic, List, Optional, TypeVar

from errorcollector.error_collector import MultipleErrorCollector, SingleErrorCollector
from godslayer.exceptions import InvalidRecordError

from zaimcsvconverter.exceptions import UndefinedContentError
from zaimcsvconverter.file_csv_convert import FileCsvConvertContext
from zaimcsvconverter.models import FileCsvConvertId, Item, Store


# @see https://github.com/python/mypy/issues/5374
@dataclass
class InputRowData:  # type: ignore
    """This class is abstract class of input CSV row data."""

    list_error: List[InvalidRecordError] = field(default_factory=list, init=False)
    undefined_content_error: Optional[UndefinedContentError] = field(default=None, init=False)

    @property
    @abstractmethod
    def date(self) -> datetime:
        """This property returns date as datetime."""

    @property
    @abstractmethod
    def validate(self) -> bool:
        """This method validates data."""
        return bool(self.list_error) or self.undefined_content_error is not None

    def stock_error(self, method: Callable[[], Any], message: str) -> Any:
        """This method stocks error"""
        with MultipleErrorCollector(InvalidRecordError, message, self.list_error):
            return method()


# Reason: Pylint's Bug. @see https://github.com/PyCQA/pylint/issues/179 pylint: disable=abstract-method
# @see https://github.com/python/mypy/issues/5374
@dataclass
class InputStoreRowData(InputRowData, ABC):  # type: ignore
    """This class is abstract class of input CSV row data including column to find store (nullable OK)."""

    _store: Optional[Store] = field(default=None, init=False)

    @property
    @abstractmethod
    def store_name(self) -> str:
        """This property returns store name."""

    @property
    def is_empty_store_name(self) -> bool:
        """This property returns whether store name is empty or not."""
        return str.strip(self.store_name) == ""


# Reason: Pylint's Bug. @see https://github.com/PyCQA/pylint/issues/179 pylint: disable=abstract-method
# @see https://github.com/python/mypy/issues/5374
@dataclass
class InputItemRowData(InputRowData, ABC):  # type: ignore
    """This class is abstract class of input CSV row data including column to find item (nullable OK)."""

    _item: Optional[Store] = field(default=None, init=False)

    @property
    @abstractmethod
    def item_name(self) -> str:
        """This property returns item name."""


TypeVarInputRowData = TypeVar("TypeVarInputRowData", bound=InputRowData)


class InputRow(Generic[TypeVarInputRowData]):
    """This class implements row model of CSV."""

    def __init__(self, input_row_data: TypeVarInputRowData):
        self.list_error: List[InvalidRecordError] = []
        self.date: datetime = input_row_data.date

    # Reason: Parent method. pylint: disable=no-self-use
    @property
    def validate(self) -> bool:
        """This method validates data."""
        return bool(self.list_error)

    def stock_error(self, method: Callable[[], Any], message: str) -> Any:
        """This method stocks error"""
        with MultipleErrorCollector(InvalidRecordError, message, self.list_error):
            return method()

    # Reason: Parent method. pylint: disable=no-self-use
    @property
    def is_row_to_skip(self) -> bool:
        """This property returns whether this row should be skipped or not."""
        return False


class InputContentRow(InputRow):
    """Row model of CSV including at least either store or item name data."""

    @abstractmethod
    def get_report_undefined_content_error(self) -> List[List[str]]:
        raise NotImplementedError()


class InputStoreRow(InputContentRow):
    """This class implements row model of CSV including store name data (disallow empty)."""

    def __init__(self, input_store_row_data: InputStoreRowData, file_csv_convert_context_store: FileCsvConvertContext):
        super().__init__(input_store_row_data)
        self._file_csv_convert_store: FileCsvConvertContext = file_csv_convert_context_store
        self.store_name: str = input_store_row_data.store_name
        self._store: Optional[Store] = None
        self.undefined_content_error_store: Optional[UndefinedContentError] = None

    @property
    def store(self) -> Store:
        """This method finds store data from database if has not find."""
        if self._store is None:
            self._store = Store.try_to_find(self._file_csv_convert_store.id, self.store_name)
        return self._store

    def stock_undefined_content_error_store(self, method: Callable[[], Any], message: str) -> Any:
        """This method stocks undefined content error."""
        error_collector = SingleErrorCollector(UndefinedContentError, message)
        # noinspection PyUnusedLocal
        return_value = None
        with error_collector:
            return_value = method()
        self.undefined_content_error_store = error_collector.error
        if self.undefined_content_error_store is not None:
            self.list_error.insert(0, self.undefined_content_error_store)
        return return_value

    @property
    def validate(self) -> bool:
        self.stock_undefined_content_error_store(
            lambda: self.store, f"Store name has not been defined in convert table CSV. Store name = {self.store_name}"
        )
        return super().validate or self.undefined_content_error_store is not None

    def get_report_undefined_content_error(self) -> List[List[str]]:
        """This method returns report of undefined content error."""
        return (
            []
            if self.undefined_content_error_store is None
            else [[self._file_csv_convert_store.name, self.store_name, ""]]
        )


class InputItemRow(InputContentRow):
    """This class implements row model of CSV including item name data (disallow empty)."""

    def __init__(self, file_csv_convert_item: FileCsvConvertContext, input_item_row_data: InputItemRowData):
        super().__init__(input_item_row_data)
        self._file_csv_convert_item: FileCsvConvertContext = file_csv_convert_item
        self.store_name: str = ""
        self.item_name: str = input_item_row_data.item_name
        self._item: Optional[Item] = None
        self.undefined_content_error_item: Optional[UndefinedContentError] = None

    @property
    @abstractmethod
    def store(self) -> Store:
        """This property returns store in Zaim row."""

    @property
    def item(self) -> Item:
        """This method finds store data from database if has not find."""
        if self._item is None:
            self._item = Item.try_to_find(self._file_csv_convert_item.id, self.item_name)
        return self._item

    def stock_undefined_content_error_item(self, method: Callable[[], Any], message: str) -> Any:
        """This method stocks undefined content error."""
        error_collector = SingleErrorCollector(UndefinedContentError, message)
        # noinspection PyUnusedLocal
        return_value = None
        with error_collector:
            return_value = method()
        self.undefined_content_error_item = error_collector.error
        if self.undefined_content_error_item is not None:
            self.list_error.insert(0, self.undefined_content_error_item)
        return return_value

    @property
    def validate(self) -> bool:
        self.stock_undefined_content_error_item(
            lambda: self.item, f"Item name has not been defined in convert table CSV. Item name = {self.item_name}"
        )
        return super().validate or self.undefined_content_error_item is not None

    def get_report_undefined_content_error(self) -> List[List[str]]:
        """This method returns report of undefined content error."""
        return (
            []
            if self.undefined_content_error_item is None
            else [[self._file_csv_convert_item.name, "", self.item_name]]
        )


class InputStoreItemRow(InputStoreRow):
    """This class implements row model of CSV including store name and item name data (disallow empty)."""

    def __init__(
        self,
        input_item_row_data: InputItemRowData,
        file_csv_convert_context_store: FileCsvConvertContext,
        file_csv_convert_context_item: FileCsvConvertId,
    ):
        super().__init__(input_item_row_data, file_csv_convert_context_store)
        self._file_csv_convert_item: FileCsvConvertContext = file_csv_convert_context_item
        self.store_name: str = ""
        self.item_name: str = input_item_row_data.item_name
        self._item: Optional[Item] = None
        self.undefined_content_error_item: Optional[UndefinedContentError] = None

    @property
    def item(self) -> Item:
        """This method finds store data from database if has not find."""
        if self._item is None:
            self._item = Item.try_to_find(self._file_csv_convert_item.id, self.item_name)
        return self._item

    def stock_undefined_content_error_item(self, method: Callable[[], Any], message: str) -> Any:
        """This method stocks undefined content error."""
        error_collector = SingleErrorCollector(UndefinedContentError, message)
        # noinspection PyUnusedLocal
        return_value = None
        with error_collector:
            return_value = method()
        self.undefined_content_error_item = error_collector.error
        if self.undefined_content_error_item is not None:
            self.list_error.insert(0, self.undefined_content_error_item)
        return return_value

    @property
    def validate(self) -> bool:
        self.stock_undefined_content_error_item(
            lambda: self.item, f"Item name has not been defined in convert table CSV. Item name = {self.item_name}"
        )
        return super().validate or self.undefined_content_error_item is not None

    def get_report_undefined_content_error(self) -> List[str]:
        """This method returns report of undefined content error."""
        report_undefined_content_error = super().get_report_undefined_content_error()
        if self.undefined_content_error_item is not None:
            report_undefined_content_error.append([self._file_csv_convert_item.name, "", self.item_name])
        return report_undefined_content_error


TypeVarInputRow = TypeVar("TypeVarInputRow", bound=InputRow)
TypeVarInputContentRow = TypeVar("TypeVarInputContentRow", bound=InputContentRow)


class InputRowFactory(Generic[TypeVarInputRowData, TypeVarInputRow]):
    """
    This class implements factory to create input CSV row instance.
    Why factory class is independent from input row data class is
    because we can't achieve 100% coverage without this factory.
    When model instance on post process depend on pre process,
    In nature, best practice to generate model instance on post process is
    to implement create method into each model on pre process.
    Then, pre process will depend on post process.
    And when add type hint to argument of __init__ method on model on post process,
    circular dependency occurs.
    To resolve it, we need to use TYPE_CHECKING,
    however, pytest-cov detect import line only for TYPE_CHECKING as uncovered row.
    @see https://github.com/python/mypy/issues/6101
    """

    @abstractmethod
    def create(self, input_row_data: TypeVarInputRowData) -> TypeVarInputRow:
        """This method creates input row by input CSV row data."""
