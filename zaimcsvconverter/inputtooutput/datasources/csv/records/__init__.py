"""This module implements row model of CSV."""
from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Any, Callable, Generic, Optional, TypeVar

from errorcollector import MultipleErrorCollector, SingleErrorCollector

from zaimcsvconverter.exceptions import InvalidCellError, UndefinedContentError
from zaimcsvconverter.file_csv_convert import FileCsvConvertContext
from zaimcsvconverter.inputtooutput.datasources import AbstractInputRecord
from zaimcsvconverter.inputtooutput.datasources.csv.data import (
    TypeVarInputItemRowData,
    TypeVarInputRowData,
    TypeVarInputStoreItemRowData,
    TypeVarInputStoreRowData,
)
from zaimcsvconverter.models import Item, Store


class InputRow(Generic[TypeVarInputRowData], AbstractInputRecord):
    """This class implements row model of CSV."""

    def __init__(self, input_row_data: TypeVarInputRowData):
        self.list_error: list[InvalidCellError] = []
        self.date: datetime = input_row_data.date

    # Reason: Parent method. pylint: disable=no-self-use
    @property
    def validate(self) -> bool:
        """This method validates data."""
        return bool(self.list_error)

    def stock_error(self, method: Callable[[], Any], message: str) -> Any:
        """This method stocks error."""
        with MultipleErrorCollector(InvalidCellError, message, self.list_error):
            return method()

    # Reason: Parent method. pylint: disable=no-self-use
    @property
    def is_row_to_skip(self) -> bool:
        """This property returns whether this row should be skipped or not."""
        return False


class InputContentRow(InputRow[TypeVarInputRowData]):
    """Row model of CSV including at least either store or item name data."""

    @abstractmethod
    def get_report_undefined_content_error(self) -> list[list[str]]:
        raise NotImplementedError()


class InputStoreRow(InputContentRow[TypeVarInputStoreRowData]):
    """This class implements row model of CSV including store name data (disallow empty)."""

    def __init__(
        self, input_store_row_data: TypeVarInputStoreRowData, file_csv_convert_context_store: FileCsvConvertContext
    ):
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

    def get_report_undefined_content_error(self) -> list[list[str]]:
        """This method returns report of undefined content error."""
        return (
            []
            if self.undefined_content_error_store is None
            else [[self._file_csv_convert_store.name, self.store_name, ""]]
        )


class InputItemRow(InputContentRow[TypeVarInputItemRowData]):
    """This class implements row model of CSV including item name data (disallow empty)."""

    def __init__(self, file_csv_convert_item: FileCsvConvertContext, input_item_row_data: TypeVarInputItemRowData):
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

    def get_report_undefined_content_error(self) -> list[list[str]]:
        """This method returns report of undefined content error."""
        return (
            []
            if self.undefined_content_error_item is None
            else [[self._file_csv_convert_item.name, "", self.item_name]]
        )


class InputStoreItemRow(InputStoreRow[TypeVarInputStoreItemRowData]):
    """This class implements row model of CSV including store name and item name data (disallow empty)."""

    def __init__(
        self,
        input_store_item_row_data: TypeVarInputStoreItemRowData,
        file_csv_convert_context_store: FileCsvConvertContext,
        file_csv_convert_context_item: FileCsvConvertContext,
    ):
        super().__init__(input_store_item_row_data, file_csv_convert_context_store)
        self._file_csv_convert_item: FileCsvConvertContext = file_csv_convert_context_item
        self.store_name: str = ""
        self.item_name: str = input_store_item_row_data.item_name
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

    def get_report_undefined_content_error(self) -> list[list[str]]:
        """This method returns report of undefined content error."""
        report_undefined_content_error = super().get_report_undefined_content_error()
        if self.undefined_content_error_item is not None:
            report_undefined_content_error.append([self._file_csv_convert_item.name, "", self.item_name])
        return report_undefined_content_error


TypeVarInputRow = TypeVar("TypeVarInputRow", bound=InputRow[Any])
TypeVarInputContentRow = TypeVar("TypeVarInputContentRow", bound=InputContentRow[Any])
TypeVarInputStoreRow = TypeVar("TypeVarInputStoreRow", bound=InputStoreRow[Any])
TypeVarInputItemRow = TypeVar("TypeVarInputItemRow", bound=InputItemRow[Any])
TypeVarInputStoreItemRow = TypeVar("TypeVarInputStoreItemRow", bound=InputStoreItemRow[Any])
