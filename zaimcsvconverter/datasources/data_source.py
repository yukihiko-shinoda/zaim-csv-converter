"""This module implements data source model."""
from abc import ABC, abstractmethod
from typing import Generator, List, Any, Dict

from godslayer.exceptions import InvalidRecordError


class DataSource(ABC):
    """This class implements data source model."""
    def __init__(self):
        self.dictionary_invalid_record: Dict[int, List[InvalidRecordError]] = {}

    @abstractmethod
    def __iter__(self) -> Generator[List[Any], None, None]:
        raise NotImplementedError()  # pragma: no cover

    @abstractmethod
    def mark_current_record_as_error(self, list_error: List[InvalidRecordError]):
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
