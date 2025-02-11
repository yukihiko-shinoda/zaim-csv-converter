"""Converter from CSV data to record model."""

from abc import abstractmethod
from typing import Generic

from returns.primitives.hkt import Kind1

from zaimcsvconverter.inputtooutput.datasources.csvfile.data import TypeVarInputRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import TypeVarInputRow


class InputRowFactory(Generic[TypeVarInputRowData, TypeVarInputRow]):
    """This class implements factory to create input CSV row instance.

    Why factory class is independent from input row data class is because we can't achieve 100% coverage without this
    factory. When model instance on post process depend on pre process, In nature, best practice to generate model
    instance on post process is to implement create method into each model on pre process. Then, pre process will
    depend on post process. And when add type hint to argument of __init__ method on model on post process, circular
    dependency occurs. To resolve it, we need to use TYPE_CHECKING, however, pytest-cov detect import line only for
    TYPE_CHECKING as uncovered row.

    @see
    https://github.com/python/mypy/issues/6101
    """

    @abstractmethod
    def create(self, input_row_data: TypeVarInputRowData) -> Kind1[TypeVarInputRow, TypeVarInputRowData]:
        """This method creates input row by input CSV row data."""
