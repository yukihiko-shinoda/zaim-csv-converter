"""This module implements constants which suitable module to belong is not defined."""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Type, List, Any, Generic, Optional

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats import InputRowData, InputRow, TypeVarInputRowData, TypeVarInputRow, \
    InputRowFactory
from zaimcsvconverter.inputcsvformats.amazon import AmazonRowData, AmazonRowFactory
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRowData, GoldPointCardPlusRowFactory
from zaimcsvconverter.inputcsvformats.mufg import MufgRowData, MufgRowFactory
from zaimcsvconverter.inputcsvformats.sf_card_viewer import SFCardViewerRowData, SFCardViewerRowFactory
from zaimcsvconverter.inputcsvformats.waon import WaonRowData, WaonRowFactory
from zaimcsvconverter.models import AccountId, ConvertTableType, ConvertTableRecordMixin
from zaimcsvconverter.rowconverters.amazon import AmazonZaimRowConverterSelector
from zaimcsvconverter.rowconverters.sf_card_viewer import SFCardViewerZaimRowConverterSelector
from zaimcsvconverter.rowconverters.gold_point_card_plus import GoldPointCardPlusZaimRowConverterSelector
from zaimcsvconverter.rowconverters.mufg import MufgZaimRowConverterSelector
from zaimcsvconverter.rowconverters.waon import WaonZaimRowConverterSelector
from zaimcsvconverter.rowconverters import ZaimRowConverterSelector


class FileNameCsvConvert(Enum):
    """This class implements file name of CSV file for convert table data."""
    WAON = 'waon.csv'
    GOLD_POINT_CARD_PLUS = 'gold_point_card_plus.csv'
    MUFG = 'mufg.csv'
    PASMO = 'sf_card_viewer.csv'
    AMAZON = 'amazon.csv'

    @property
    def value(self) -> str:
        """This method overwrite super method for type hint."""
        return super().value


@dataclass
class AccountContext(Generic[TypeVarInputRowData, TypeVarInputRow]):
    """This class implements recipe for converting steps for WAON CSV."""
    id: AccountId
    file_name_csv_convert: FileNameCsvConvert
    regex_csv_file_name: str
    # @see https://github.com/PyCQA/pylint/issues/2416
    # pylint: disable=unsubscriptable-object
    convert_table_type: ConvertTableType
    # pylint: disable=unsubscriptable-object
    input_row_data_class: Type[TypeVarInputRowData]
    input_row_factory: InputRowFactory[TypeVarInputRowData, TypeVarInputRow]
    zaim_row_converter_selector: ZaimRowConverterSelector[TypeVarInputRow]
    encode: str = 'UTF-8'
    csv_header: Optional[List[str]] = None

    def create_convert_table_row_instance(
            self, list_convert_table_row_standard_type_value: List[Any]
    ) -> ConvertTableRecordMixin:
        """This method creates convert table row model instance by list data of convert table row."""
        convert_table_type = self.convert_table_type.value
        return convert_table_type.model(
            self.id, convert_table_type.row_data(*list_convert_table_row_standard_type_value)
        )

    def create_input_row_instance(self, input_row_data: TypeVarInputRowData) -> TypeVarInputRow:
        """This method creates input row instance by input row data instance."""
        return self.input_row_factory.create(self.id, input_row_data)


class Account(Enum):
    """This class implements constant of account in Zaim."""
    WAON = AccountContext(
        AccountId.WAON,
        FileNameCsvConvert.WAON,
        r'.*waon.*\.csv',
        ConvertTableType.STORE,
        WaonRowData,
        WaonRowFactory(),
        WaonZaimRowConverterSelector(),
        'UTF-8',
        ['取引年月日', '利用店舗', '利用金額（税込）', '利用区分', 'チャージ区分']
    )
    GOLD_POINT_CARD_PLUS = AccountContext(
        AccountId.GOLD_POINT_CARD_PLUS,
        FileNameCsvConvert.GOLD_POINT_CARD_PLUS,
        r'.*gold_point_card_plus.*\.csv',
        ConvertTableType.STORE,
        GoldPointCardPlusRowData,
        GoldPointCardPlusRowFactory(),
        GoldPointCardPlusZaimRowConverterSelector(),
        'shift_jis_2004'
    )
    MUFG = AccountContext(
        AccountId.MUFG,
        FileNameCsvConvert.MUFG,
        r'.*mufg.*\.csv',
        ConvertTableType.STORE,
        MufgRowData,
        MufgRowFactory(),
        MufgZaimRowConverterSelector(),
        'shift_jis_2004',
        ['日付', '摘要', '摘要内容', '支払い金額', '預かり金額', '差引残高', 'メモ', '未資金化区分', '入払区分']
    )
    PASMO = AccountContext(
        AccountId.PASMO,
        FileNameCsvConvert.PASMO,
        r'.*pasmo.*\.csv',
        ConvertTableType.STORE,
        SFCardViewerRowData,
        # On this timing, CONFIG is not loaded. So we wrap CONFIG by lambda.
        SFCardViewerRowFactory(lambda: CONFIG.pasmo),
        SFCardViewerZaimRowConverterSelector(lambda: CONFIG.pasmo),
        'shift_jis_2004',
        ['利用年月日', '定期', '鉄道会社名', '入場駅/事業者名', '定期', '鉄道会社名', '出場駅/降車場所', '利用額(円)', '残額(円)', 'メモ']
    )
    AMAZON = AccountContext(
        AccountId.AMAZON,
        FileNameCsvConvert.AMAZON,
        r'.*amazon.*\.csv',
        ConvertTableType.ITEM,
        AmazonRowData,
        AmazonRowFactory(),
        AmazonZaimRowConverterSelector(),
        'utf-8-sig',
        [
            '注文日', '注文番号', '商品名', '付帯情報', '価格', '個数', '商品小計', '注文合計',
            'お届け先', '状態', '請求先', '請求額', 'クレカ請求日', 'クレカ請求額', 'クレカ種類',
            '注文概要URL', '領収書URL', '商品URL'
        ]
    )

    @property
    def value(self) -> AccountContext:
        """This method overwrite super method for type hint."""
        return super().value

    @staticmethod
    def create_by_path_csv_convert(path: Path) -> Account:
        """This method creates Enum instance by path to CSV convert file."""
        # noinspection PyUnusedLocal
        account: Account
        for account in Account:
            if path.name == account.value.file_name_csv_convert.value:
                return account
        raise ValueError("can't detect account type by csv file name. Please confirm csv file name.")

    @staticmethod
    def create_by_path_csv_input(path: Path) -> Account:
        """This function create correct setting instance by argument."""
        # noinspection PyUnusedLocal
        account: Account
        for account in Account:
            if re.search(account.value.regex_csv_file_name, path.name):
                return account
        raise ValueError("can't detect account type by csv file name. Please confirm csv file name.")

    def create_convert_table_row_instance(
            self, list_convert_table_row_standard_type_value: List[Any]
    ) -> ConvertTableRecordMixin:
        """This method creates convert table row model instance by list data of convert table row."""
        return self.value.create_convert_table_row_instance(list_convert_table_row_standard_type_value)

    def create_input_row_data_instance(self, list_input_row_standard_type_value: List[str]) -> InputRowData:
        """This method creates input row data instance by list data of input row."""
        return self.value.input_row_data_class(*list_input_row_standard_type_value)

    def create_input_row_instance(self, input_row_data: InputRowData) -> InputRow:
        """This method creates input row instance by input row data instance."""
        return self.value.create_input_row_instance(input_row_data)
