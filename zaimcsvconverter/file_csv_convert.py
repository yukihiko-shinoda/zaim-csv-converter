"""This module implements CSV file for convert table."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from types import DynamicClassAttribute

from zaimcsvconverter.models import (
    Base,
    ConvertTableRecordMixin,
    ConvertTableRowData,
    ConvertTableType,
    FileCsvConvertId,
)


@dataclass
class FileCsvConvertContext:
    """This class implements CSV file for convert table."""

    # pylint:disable=invalid-name
    id: FileCsvConvertId
    name: str
    convert_table_type: ConvertTableType

    def create_convert_table_row_instance(
        self,
        list_convert_table_row_standard_type_value: list[str],
    ) -> ConvertTableRecordMixin[Base, ConvertTableRowData]:
        """This method creates convert table row model instance by list data of convert table row."""
        convert_table_type = self.convert_table_type.value
        # noinspection PyArgumentList
        return convert_table_type.model(
            self.id,
            convert_table_type.row_data(*list_convert_table_row_standard_type_value),
        )


class FileCsvConvert(Enum):
    """This class implements file name of CSV file for convert table data."""

    WAON = FileCsvConvertContext(FileCsvConvertId.WAON, "waon.csv", ConvertTableType.STORE)
    GOLD_POINT_CARD_PLUS = FileCsvConvertContext(
        FileCsvConvertId.GOLD_POINT_CARD_PLUS,
        "gold_point_card_plus.csv",
        ConvertTableType.STORE,
    )
    MUFG = FileCsvConvertContext(FileCsvConvertId.MUFG, "mufg.csv", ConvertTableType.STORE)
    SF_CARD_VIEWER = FileCsvConvertContext(
        FileCsvConvertId.SF_CARD_VIEWER,
        "sf_card_viewer.csv",
        ConvertTableType.STORE,
    )
    AMAZON = FileCsvConvertContext(FileCsvConvertId.AMAZON, "amazon.csv", ConvertTableType.ITEM)
    VIEW_CARD = FileCsvConvertContext(FileCsvConvertId.VIEW_CARD, "view_card.csv", ConvertTableType.STORE)
    PAY_PAL_STORE = FileCsvConvertContext(FileCsvConvertId.PAY_PAL, "pay_pal_store.csv", ConvertTableType.STORE)
    PAY_PAL_ITEM = FileCsvConvertContext(FileCsvConvertId.PAY_PAL, "pay_pal_item.csv", ConvertTableType.ITEM)
    SBI_SUMISHIN_NET_BANK = FileCsvConvertContext(
        FileCsvConvertId.SBI_SUMISHIN_NET_BANK,
        "sbi_sumishin_net_bank.csv",
        ConvertTableType.STORE,
    )
    PAY_PAY_CARD = FileCsvConvertContext(FileCsvConvertId.PAY_PAY_CARD, "pay_pay_card.csv", ConvertTableType.STORE)
    MOBILE_SUICA = FileCsvConvertContext(FileCsvConvertId.MOBILE_SUICA, "mobile_suica.csv", ConvertTableType.STORE)

    @DynamicClassAttribute
    def value(self) -> FileCsvConvertContext:
        """This method overwrite super method for type hint."""
        return super().value

    @staticmethod
    def create_by_path_csv_convert(path: Path) -> FileCsvConvert:
        """This method creates Enum instance by path to CSV convert file."""
        for file_csv_convert in FileCsvConvert:
            if path.name == file_csv_convert.value.name:
                return file_csv_convert
        raise ValueError("can't detect account type by csv file name. Please confirm csv file name.")

    def create_convert_table_row_instance(
        self,
        list_convert_table_row_standard_type_value: list[str],
    ) -> ConvertTableRecordMixin[Base, ConvertTableRowData]:
        """This method creates convert table row model instance by list data of convert table row."""
        return self.value.create_convert_table_row_instance(list_convert_table_row_standard_type_value)
