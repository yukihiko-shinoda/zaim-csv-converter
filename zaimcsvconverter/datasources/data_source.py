"""This module implements data source model."""
from abc import ABC, abstractmethod
from typing import Dict, Generator, Generic, List

from returns.primitives.hkt import Kind1

from zaimcsvconverter.errorhandling.error_handler import UndefinedContentErrorHandler
from zaimcsvconverter.exceptions import InvalidCellError
from zaimcsvconverter.inputcsvformats import TypeVarInputRow, TypeVarInputRowData


class DataSource(Generic[TypeVarInputRow, TypeVarInputRowData], ABC):
    """This class implements data source model."""

    def __init__(self) -> None:
        self.dictionary_invalid_record: Dict[int, List[InvalidCellError]] = {}
        self.undefined_content_error_handler = UndefinedContentErrorHandler()

    @abstractmethod
    def __iter__(self) -> Generator[Kind1[TypeVarInputRow, TypeVarInputRowData], None, None]:
        raise NotImplementedError()  # pragma: no cover

    @abstractmethod
    def mark_current_record_as_error(self, list_error: List[InvalidCellError]) -> None:
        """Marks current record as error."""
        raise NotImplementedError()  # pragma: no cover

    @property
    @abstractmethod
    def is_invalid(self) -> bool:
        """Returns whether this data source is invalid or not."""
        raise NotImplementedError()  # pragma: no cover

    @abstractmethod
    def raise_error_if_invalid(self) -> None:
        """Raises error if this data source is invalid."""
        raise NotImplementedError()  # pragma: no cover
