"""Abstract output model exporter."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from zaimcsvconverter.context_manager import ContextManager


# Reason: Abstract class to support other application than Zaim pylint: disable=too-few-public-methods
class OutputRecord(ABC):  # noqa: B024
    pass


TypeVarOutputRecord = TypeVar("TypeVarOutputRecord", bound=OutputRecord)


class OutputModelExporter(Generic[TypeVarOutputRecord], ContextManager[Any], ABC):
    @abstractmethod
    def execute(self, output_row: TypeVarOutputRecord) -> None:
        raise NotImplementedError


TypeVarOutputModelExporter = TypeVar("TypeVarOutputModelExporter", bound=OutputModelExporter[Any])
