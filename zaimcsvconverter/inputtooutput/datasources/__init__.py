"""To handle data source by abstraction for compatibility in future."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from zaimcsvconverter.errorhandling.error_handler import UndefinedContentErrorHandler

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Generator

    from zaimcsvconverter.exceptions import InvalidCellError


# Reason: Abstract class. pylint: disable=too-few-public-methods
class AbstractInputRecord(ABC):  # noqa: B024
    """This class implements input record model."""


class DataSource(ABC):
    """This class implements data source model."""

    def __init__(self) -> None:
        self.dictionary_invalid_record: dict[int, list[InvalidCellError]] = {}
        self.undefined_content_error_handler = UndefinedContentErrorHandler()

    @abstractmethod
    def __iter__(self) -> Generator[AbstractInputRecord, None, None]:
        raise NotImplementedError

    @abstractmethod
    def mark_current_record_as_error(self, list_error: list[InvalidCellError]) -> None:
        """Marks current record as error."""
        raise NotImplementedError

    @property
    @abstractmethod
    def is_invalid(self) -> bool:
        """Returns whether this data source is invalid or not."""
        raise NotImplementedError

    @property
    @abstractmethod
    def message(self) -> str:
        """Raises error if this data source is invalid."""
        raise NotImplementedError
