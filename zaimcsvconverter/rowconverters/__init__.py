"""This module implements convert steps from input row to Zaim row."""
from abc import ABC, abstractmethod
from typing import cast, Generic, Optional, TypeVar

from returns.primitives.hkt import Kind1, kinded

from zaimcsvconverter.inputcsvformats import (
    TypeVarInputItemRow,
    TypeVarInputItemRowData,
    TypeVarInputRow,
    TypeVarInputRowData,
    TypeVarInputStoreItemRow,
    TypeVarInputStoreItemRowData,
    TypeVarInputStoreRow,
    TypeVarInputStoreRowData,
)
from zaimcsvconverter.inputtooutput.datasources import AbstractInputRecord
from zaimcsvconverter.inputtooutput.exporters.zaim.csv.zaim_csv_format import ZaimCsvFormat


class AbstractZaimRowConverter(ABC):
    pass


TypeVarAbstractZaimRowConverter = TypeVar("TypeVarAbstractZaimRowConverter", bound=AbstractZaimRowConverter)


# Reason: Abstract class. pylint: disable=too-few-public-methods
class ZaimRowConverter(Generic[TypeVarInputRow, TypeVarInputRowData], AbstractZaimRowConverter, ABC):
    """This class implements convert steps from input row to Zaim row."""

    def __init__(self, input_row: Kind1[TypeVarInputRow, TypeVarInputRowData]):
        self.input_row = cast(TypeVarInputRow, self.to_container(input_row))

    @kinded
    @classmethod
    def to_container(
        cls, input_row: Kind1[TypeVarInputRow, TypeVarInputRowData]
    ) -> Kind1[TypeVarInputRow, TypeVarInputRowData]:
        # To check type of TypeVarInputRowData (probably...)
        return input_row


class ZaimIncomeRowConverter(ZaimRowConverter[TypeVarInputRow, TypeVarInputRowData]):
    """This class implements convert steps from input row to Zaim income row."""

    @property
    @abstractmethod
    def category(self) -> str:
        """This property returns category on Zaim income row."""

    @property
    @abstractmethod
    def store_name(self) -> str:
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
    def category(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.category_income

    @property
    def store_name(self) -> str:
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
    def store_name(self) -> str:
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
    def store_name(self) -> str:
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
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.item.name

    @property
    def store_name(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.name_zaim


class ZaimPaymentRowStoreItemConverter(
    ZaimPaymentRowConverter[TypeVarInputStoreItemRow, TypeVarInputStoreItemRowData], ABC
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
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.item.name

    @property
    def store_name(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.name_zaim


class ZaimTransferRowConverter(ZaimRowConverter[TypeVarInputRow, TypeVarInputRowData]):
    """This class implements convert steps from input row to Zaim transfer row."""

    @property
    @abstractmethod
    def cash_flow_source(self) -> str:
        """This property returns cash flow source."""

    @property
    @abstractmethod
    def cash_flow_target(self) -> str:
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

    @see https://github.com/python/mypy/issues/6101
    """

    def create(self, input_row: AbstractInputRecord) -> AbstractZaimRowConverter:
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

    @see https://github.com/python/mypy/issues/6101
    """

    # Reason: Maybe, there are no way to resolve.
    # The nearest issues: https://github.com/dry-python/returns/issues/708
    def create(  # type: ignore
        self,
        input_row: Kind1[TypeVarInputRow, TypeVarInputRowData],
    ) -> ZaimRowConverter[TypeVarInputRow, TypeVarInputRowData]:
        """This method selects Zaim row converter."""
        raise NotImplementedError
