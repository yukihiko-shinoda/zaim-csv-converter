"""Abstract output model exporter."""
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from zaimcsvconverter.context_manager import ContextManager
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import TypeVarAbstractOutputRow


class OutputModelExporter(Generic[TypeVarAbstractOutputRow], ContextManager[Any], ABC):
    @abstractmethod
    def execute(self, output_row: TypeVarAbstractOutputRow) -> None:
        raise NotImplementedError


TypeVarOutputModelExporter = TypeVar("TypeVarOutputModelExporter", bound=OutputModelExporter[Any])
