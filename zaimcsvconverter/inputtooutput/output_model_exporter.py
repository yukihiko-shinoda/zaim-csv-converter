"""Abstract output model exporter."""
from abc import ABC, abstractmethod
from typing import Generic

from zaimcsvconverter.zaim.zaim_row import TypeVarAbstractOutputRow


class OutputModelExporter(Generic[TypeVarAbstractOutputRow], ABC):
    @abstractmethod
    def execute(self, output_row: TypeVarAbstractOutputRow) -> None:
        raise NotImplementedError
