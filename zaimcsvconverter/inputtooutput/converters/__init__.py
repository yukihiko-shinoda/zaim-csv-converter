"""Abstract record converter."""

from abc import ABC, abstractmethod

from zaimcsvconverter.inputtooutput.datasources import AbstractInputRecord
from zaimcsvconverter.inputtooutput.exporters import OutputRecord


class RecordConverter(ABC):
    @abstractmethod
    def convert(self, input_record: AbstractInputRecord) -> OutputRecord:
        raise NotImplementedError
