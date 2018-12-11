#!/usr/bin/env python
"""This module implements iterating steps from input_csv_converter."""
import csv
from pathlib import Path
from typing import NoReturn, List

import numpy

from zaimcsvconverter.account import DirectoryCsv
from zaimcsvconverter.input_csv_converter import InputCsvConverter


class InputCsvConverterIterator:
    """This class implements iterating steps from input_csv_converter."""
    FILE_NAME_ERROR = 'error.csv'

    def __init__(
            self,
            directory_csv_input: Path = DirectoryCsv.INPUT.value,
            directory_csv_output: Path = DirectoryCsv.OUTPUT.value,
    ):
        self.directory_csv_input = directory_csv_input
        self.directory_csv_output = directory_csv_output

    def execute(self) -> NoReturn:
        """This method executes all CSV converters."""
        list_csv_converter: List[InputCsvConverter] = []
        for path in self.directory_csv_input.glob('*.csv'):
            list_csv_converter.append(InputCsvConverter(path, self.directory_csv_output))
        list_undefined_store = []
        for csv_converter in list_csv_converter:
            try:
                csv_converter.execute()
            except KeyError:
                list_undefined_store.extend(csv_converter.list_undefined_content)
                continue
        if list_undefined_store:
            list_undefined_store = numpy.unique(list_undefined_store, axis=0).tolist()
            with (self.directory_csv_output / self.FILE_NAME_ERROR).open(
                    'w', encoding='UTF-8', newline='\n'
            ) as file_error:
                writer_error = csv.writer(file_error)
                for undefined_store in list_undefined_store:
                    writer_error.writerow(undefined_store)
            raise KeyError(f'Undefined store name in convert table CSV exists. Please check {self.FILE_NAME_ERROR}.')
