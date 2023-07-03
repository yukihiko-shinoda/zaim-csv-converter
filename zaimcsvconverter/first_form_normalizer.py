"""Generator to iterate CSV row data as model instance."""
from collections.abc import Generator
from logging import getLogger
from pathlib import Path
from typing import Generic, TypeVar

from godslayer.csv.god_slayer import GodSlayer
from pydantic.dataclasses import dataclass


@dataclass
class CsvRowData:
    """This class is abstract class of input CSV row data."""


T = TypeVar("T", bound=CsvRowData)  # pylint: disable=invalid-name


class FirstFormNormalizer(Generic[T]):
    """Generator to iterate CSV row data as model instance."""

    def __init__(
        self,
        god_slayer: GodSlayer,
        input_row_data_class: type[T],
    ) -> None:
        super().__init__()
        self.god_slayer = god_slayer
        self.input_row_data_class = input_row_data_class
        self.logger = getLogger(__name__)

    def __iter__(self) -> Generator[T, None, None]:
        iterator = self.god_slayer.__iter__()
        while True:
            try:
                list_input_row_standard_type_value = next(iterator)
            except StopIteration:
                break
            self.logger.debug("self.input_row_data_class: %s", self.input_row_data_class)
            self.logger.debug("list_input_row_standard_type_value: %s", list_input_row_standard_type_value)
            yield self.input_row_data_class(*list_input_row_standard_type_value)

    @property
    def index(self) -> int:
        return self.god_slayer.index

    @property
    def path_to_file(self) -> Path:
        return self.god_slayer.path_to_file
