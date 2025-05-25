"""This module implements convert steps from input row to Zaim row."""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Generic, Optional, TypeVar, cast

from returns.primitives.hkt import Kind1, kinded

from zaimcsvconverter.exceptions import LogicError
from zaimcsvconverter.inputtooutput.datasources import AbstractInputRecord
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import (
    TypeVarInputItemRowData,
    TypeVarInputRowData,
    TypeVarInputStoreItemRowData,
    TypeVarInputStoreRowData,
)
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import (
    TypeVarInputItemRow,
    TypeVarInputRow,
    TypeVarInputStoreItemRow,
    TypeVarInputStoreRow,
)
from zaimcsvconverter.inputtooutput.exporters.zaim.csvfile.zaim_csv_format import ZaimCsvFormat
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import (
    ZaimIncomeRow,
    ZaimPaymentRow,
    ZaimRow,
    ZaimTransferRow,
)


# Reason: Abstract class. pylint: disable=too-few-public-methods
class AbstractZaimRowConverter(ABC):  # noqa: B024
    pass


TypeVarAbstractZaimRowConverter = TypeVar("TypeVarAbstractZaimRowConverter", bound=AbstractZaimRowConverter)


# Reason: Abstract class. pylint: disable=too-few-public-methods
class ZaimRowConverter(Generic[TypeVarInputRow, TypeVarInputRowData], AbstractZaimRowConverter, ABC):
    """This class implements convert steps from input row to Zaim row."""

    def __init__(self, input_row: Kind1[TypeVarInputRow, TypeVarInputRowData]) -> None:
        self.input_row = cast("TypeVarInputRow", self.to_container(input_row))

    @kinded
    @classmethod
    def to_container(
        cls,
        input_row: Kind1[TypeVarInputRow, TypeVarInputRowData],
    ) -> Kind1[TypeVarInputRow, TypeVarInputRowData]:
        """To check type of TypeVarInputRowData (probably...)"""
        return input_row

    @property
    def date(self) -> datetime:
        return self.input_row.date


class ZaimIncomeRowConverter(ZaimRowConverter[TypeVarInputRow, TypeVarInputRowData]):
    """This class implements convert steps from input row to Zaim income row."""

    @property
    @abstractmethod
    def category(self) -> Optional[str]:
        """This property returns category on Zaim income row."""

    @property
    @abstractmethod
    def store_name(self) -> Optional[str]:
        """This property returns store name."""

    @property
    @abstractmethod
    def cash_flow_target(self) -> str:
        """This property returns income cash flow target."""

    @property
    @abstractmethod
    def amount(self) -> int:
        """This property returns income amount income."""


# Reason: Pylint's Bug. @see https://github.com/PyCQA/pylint/issues/179 pylint: disable=abstract-method
class ZaimIncomeRowStoreConverter(ZaimIncomeRowConverter[TypeVarInputStoreRow, TypeVarInputStoreRowData], ABC):
    """This class implements convert steps from input store row to Zaim income row."""

    @property
    def category(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.category_income

    @property
    def store_name(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.name_zaim


class ZaimPaymentRowConverter(ZaimRowConverter[TypeVarInputRow, TypeVarInputRowData]):
    """This class implements convert steps from input row to Zaim payment row."""

    @property
    @abstractmethod
    def category_large(self) -> Optional[str]:
        """This property returns large category on Zaim payment row."""

    @property
    @abstractmethod
    def category_small(self) -> Optional[str]:
        """This property returns small category on Zaim payment row."""

    @property
    @abstractmethod
    def item_name(self) -> str:
        """This property returns item name."""

    @property
    @abstractmethod
    def store_name(self) -> Optional[str]:
        """This property returns store name."""

    @property
    @abstractmethod
    def cash_flow_source(self) -> str:
        """This property returns cash flow source."""

    @property
    def note(self) -> str:
        """This property returns note."""
        return ZaimCsvFormat.NOTE_EMPTY

    @property
    @abstractmethod
    def amount(self) -> int:
        """This property returns amount payment."""


class ZaimPaymentRowStoreConverter(ZaimPaymentRowConverter[TypeVarInputStoreRow, TypeVarInputStoreRowData], ABC):
    """This class implements convert steps from input store row to Zaim payment row."""

    @property
    def category_large(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.category_payment_large

    @property
    def category_small(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.category_payment_small

    @property
    def item_name(self) -> str:
        return ZaimCsvFormat.ITEM_NAME_EMPTY

    @property
    def store_name(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.name_zaim


class ZaimPaymentRowItemConverter(ZaimPaymentRowConverter[TypeVarInputItemRow, TypeVarInputItemRowData], ABC):
    """This class implements convert steps from input item row to Zaim payment row."""

    @property
    def category_large(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.item.category_payment_large

    @property
    def category_small(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.item.category_payment_small

    @property
    def item_name(self) -> str:
        if not self.input_row.item.name:
            msg = "Item name is empty."
            raise LogicError(msg)
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.item.name

    @property
    def store_name(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.name_zaim


class ZaimPaymentRowStoreItemConverter(
    ZaimPaymentRowConverter[TypeVarInputStoreItemRow, TypeVarInputStoreItemRowData],
    ABC,
):
    """This class implements convert steps from input store item row to Zaim payment row."""

    @property
    def category_large(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.item.category_payment_large

    @property
    def category_small(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.item.category_payment_small

    @property
    def item_name(self) -> str:
        if not self.input_row.item.name:
            msg = "Item name is empty."
            raise LogicError(msg)
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.item.name

    @property
    def store_name(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.name_zaim


class ZaimTransferRowConverter(ZaimRowConverter[TypeVarInputRow, TypeVarInputRowData]):
    """This class implements convert steps from input row to Zaim transfer row."""

    @property
    @abstractmethod
    def cash_flow_source(self) -> Optional[str]:
        """This property returns cash flow source."""

    @property
    @abstractmethod
    def cash_flow_target(self) -> Optional[str]:
        """This property returns cash flow target."""

    @property
    @abstractmethod
    def amount(self) -> int:
        """This property returns amount transfer."""


class ZaimRowConverterFactory:
    """This class implements factory of Zaim row converter.

    Why factory class is independent from input row data class is because we can't achieve 100% coverage without this
    factory. When model instance on post process depend on pre process, In nature, best practice to generate model
    instance on post process is to implement create method into each model on pre process. Then, pre process will
    depend on post process. And when add type hint to argument of __init__ method on model on post process, circular
    dependency occurs. To resolve it, we need to use TYPE_CHECKING, however, pytest-cov detect import line only for
    TYPE_CHECKING as uncovered row.

    @see
    https://github.com/python/mypy/issues/6101
    """

    def create(self, input_row: AbstractInputRecord, path_csv_file: Path) -> AbstractZaimRowConverter:
        """This method selects Zaim row converter."""
        raise NotImplementedError


class CsvRecordToZaimRowConverterFactory(Generic[TypeVarInputRow, TypeVarInputRowData], ZaimRowConverterFactory):
    """This class implements factory of Zaim row converter.

    Why factory class is independent from input row data class is because we can't achieve 100% coverage without this
    factory. When model instance on post process depend on pre process, In nature, best practice to generate model
    instance on post process is to implement create method into each model on pre process. Then, pre process will
    depend on post process. And when add type hint to argument of __init__ method on model on post process, circular
    dependency occurs. To resolve it, we need to use TYPE_CHECKING, however, pytest-cov detect import line only for
    TYPE_CHECKING as uncovered row.

    @see
    https://github.com/python/mypy/issues/6101
    """

    def create(
        self,
        # Reason: Maybe, there are no way to resolve.
        # The nearest issues: https://github.com/dry-python/returns/issues/708
        input_row: Kind1[TypeVarInputRow, TypeVarInputRowData],  # type: ignore[override]
        path_csv_file: Path,
    ) -> ZaimRowConverter[TypeVarInputRow, TypeVarInputRowData]:
        """This method selects Zaim row converter."""
        raise NotImplementedError


class ZaimRowFactory:
    """This class implements factory to create zaim format CSV row instance.

    Why factory class is independent from input row data class is because we can't achieve 100% coverage without this
    factory. When model instance on post process depend on pre process, In nature, best practice to generate model
    instance on post process is to implement create method into each model on pre process. Then, pre process will
    depend on post process. And when add type hint to argument of __init__ method on model on post process, circular
    dependency occurs. To resolve it, we need to use TYPE_CHECKING, however, pytest-cov detect import line only for
    TYPE_CHECKING as uncovered row.

    @see
    https://github.com/python/mypy/issues/6101
    """

    @staticmethod
    def create(zaim_row_converter: AbstractZaimRowConverter) -> ZaimRow:
        """This method creates Zaim row."""
        if isinstance(zaim_row_converter, ZaimIncomeRowConverter):
            return ZaimIncomeRow(zaim_row_converter)
        if isinstance(zaim_row_converter, ZaimPaymentRowConverter):
            return ZaimPaymentRow(zaim_row_converter)
        if isinstance(zaim_row_converter, ZaimTransferRowConverter):
            return ZaimTransferRow(zaim_row_converter)
        msg = f"Undefined Zaim row converter. Zaim row converter = {zaim_row_converter.__class__.__name__}"
        raise ValueError(msg)
