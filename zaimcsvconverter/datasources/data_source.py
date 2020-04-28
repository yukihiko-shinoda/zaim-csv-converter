"""This module implements data source model."""
from abc import ABC, abstractmethod
from typing import Generator, List, Any, Dict

from godslayer.exceptions import InvalidRecordError


class DataSource(ABC):
    def __init__(self):
        self.dictionary_invalid_record: Dict[int, List[InvalidRecordError]] = {}

    @abstractmethod
    def __iter__(self) -> Generator[List[Any], None, None]:
        raise NotImplementedError()  # pragma: no cover

    @abstractmethod
    def mark_current_record_as_error(self, list_error: List[InvalidRecordError]):
        raise NotImplementedError()  # pragma: no cover

    @property
    @abstractmethod
    def is_invalid(self) -> bool:
        raise NotImplementedError()  # pragma: no cover

    @abstractmethod
    def raise_error_if_invalid(self) -> None:
        raise NotImplementedError()  # pragma: no cover
