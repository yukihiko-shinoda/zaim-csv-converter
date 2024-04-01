"""Zaim CSV Converter extended CSV Data model."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, TypeVar

from pydantic.dataclasses import dataclass

from zaimcsvconverter.first_form_normalizer import CsvRowData


@dataclass
class InputRowData(CsvRowData):
    """This class is abstract class of input CSV row data."""

    @property
    @abstractmethod
    def date(self) -> datetime:
        """This property returns date as datetime."""


# Reason: Pylint's Bug. @see https://github.com/PyCQA/pylint/issues/179 pylint: disable=abstract-method
@dataclass
class InputStoreRowData(InputRowData, ABC):
    """This class is abstract class of input CSV row data including column to find store (nullable OK)."""

    @property
    @abstractmethod
    def store_name(self) -> str:
        """This property returns store name."""

    @property
    def is_empty_store_name(self) -> bool:
        """This property returns whether store name is empty or not."""
        return not str.strip(self.store_name)


# Reason: Pylint's Bug. @see https://github.com/PyCQA/pylint/issues/179 pylint: disable=abstract-method
@dataclass
class InputItemRowData(InputRowData, ABC):
    """This class is abstract class of input CSV row data including column to find item (nullable OK)."""

    @property
    @abstractmethod
    def item_name(self) -> str:
        """This property returns item name."""


# Reason: Pylint's Bug. @see https://github.com/PyCQA/pylint/issues/179 pylint: disable=abstract-method
@dataclass
class InputStoreItemRowData(InputStoreRowData, InputItemRowData, ABC):
    """This class is abstract class of input CSV row data including column to find item (nullable OK)."""


TypeVarInputRowData = TypeVar("TypeVarInputRowData", bound=InputRowData)
TypeVarInputStoreRowData = TypeVar("TypeVarInputStoreRowData", bound=InputStoreRowData)
TypeVarInputItemRowData = TypeVar("TypeVarInputItemRowData", bound=InputItemRowData)
TypeVarInputStoreItemRowData = TypeVar("TypeVarInputStoreItemRowData", bound=InputStoreItemRowData)


class RowDataFactory(Generic[TypeVarInputRowData]):
    def __init__(self, class_row_data: type[TypeVarInputRowData]) -> None:
        self.class_row_data = class_row_data

    def create(self, arg: list[str]) -> TypeVarInputRowData:
        """To seal mypy incompatible type error with pydantic typed dataclass property."""
        return self.class_row_data(*arg)
