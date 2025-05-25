"""This module implements importing process for convert table CSV."""

import csv
from pathlib import Path

from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.models import Base
from zaimcsvconverter.models import ConvertTableRecordMixin
from zaimcsvconverter.models import ConvertTableRowData


class ConvertTableImporter:
    """This class implements importing process for convert table CSV."""

    @classmethod
    def execute(cls, path: Path) -> None:
        """This method executes importing process for convert table CSV."""
        file_csv_convert = FileCsvConvert.create_by_path_csv_convert(path)
        list_convert_table = cls._load_csv(file_csv_convert, path)
        file_csv_convert.value.convert_table_type.value.model.save_all(list_convert_table)

    @classmethod
    def _load_csv(
        cls,
        file_csv_convert: FileCsvConvert,
        path: Path,
    ) -> list[ConvertTableRecordMixin[Base, ConvertTableRowData]]:
        with path.open("r", encoding="UTF-8") as file_convert_table:
            return [
                file_csv_convert.create_convert_table_row_instance(list_convert_table_row_standard_type_value)
                for list_convert_table_row_standard_type_value in csv.reader(file_convert_table)
            ]
