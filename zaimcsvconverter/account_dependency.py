"""This module implements constants which suitable module to belong is not defined."""

from __future__ import annotations

from typing import List, Union, Type
from dataclasses import dataclass

from zaimcsvconverter.input_row import InputRowFactory, InputRowData
from zaimcsvconverter.models import Store, Item


@dataclass
class AccountDependency:
    """This class implements recipe for converting steps for WAON CSV."""
    id: int
    file_name_csv_convert: str
    regex_csv_file_name: str
    # @see https://github.com/PyCQA/pylint/issues/2416
    # pylint: disable=unsubscriptable-object
    convert_table_model_class: Type[Union[Store, Item]]
    # pylint: disable=unsubscriptable-object
    input_row_data_class: Type[InputRowData]
    input_row_factory: InputRowFactory
    encode: str = 'UTF-8'
    csv_header: Union[List[str], None] = None
