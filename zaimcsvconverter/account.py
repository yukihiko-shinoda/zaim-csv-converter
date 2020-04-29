"""This module implements constants which suitable module to belong is not defined."""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Type, List, Any, Generic

from zaimcsvconverter import CONFIG
from zaimcsvconverter.datasources.csv import CsvFactory
from zaimcsvconverter.datasources.csv_with_header import CsvWithHeaderFactory
from zaimcsvconverter.datasources.view_card_csv import ViewCardCsvFactory
from zaimcsvconverter.inputcsvformats import InputRowData, InputRow, TypeVarInputRowData, TypeVarInputRow, \
    InputRowFactory
from zaimcsvconverter.inputcsvformats.amazon import AmazonRowData, AmazonRowFactory
from zaimcsvconverter.inputcsvformats.amazon_201911 import Amazon201911RowData, Amazon201911RowFactory
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRowData, GoldPointCardPlusRowFactory
from zaimcsvconverter.inputcsvformats.gold_point_card_plus_201912 import GoldPointCardPlus201912RowData, \
    GoldPointCardPlus201912RowFactory
from zaimcsvconverter.inputcsvformats.mufg import MufgRowData, MufgRowFactory
from zaimcsvconverter.inputcsvformats.sf_card_viewer import SFCardViewerRowData, SFCardViewerRowFactory
from zaimcsvconverter.inputcsvformats.view_card import ViewCardRowData, ViewCardRowFactory
from zaimcsvconverter.inputcsvformats.waon import WaonRowData, WaonRowFactory
from zaimcsvconverter.models import AccountId, ConvertTableType, ConvertTableRecordMixin
from zaimcsvconverter.rowconverters.amazon import AmazonZaimRowConverterFactory
from zaimcsvconverter.rowconverters.amazon201911 import Amazon201911ZaimRowConverterFactory
from zaimcsvconverter.rowconverters.gold_point_card_plus_201912 import GoldPointCardPlus201912ZaimRowConverterFactory
from zaimcsvconverter.rowconverters.sf_card_viewer import SFCardViewerZaimRowConverterFactory
from zaimcsvconverter.rowconverters.gold_point_card_plus import GoldPointCardPlusZaimRowConverterFactory
from zaimcsvconverter.rowconverters.mufg import MufgZaimRowConverterFactory
from zaimcsvconverter.rowconverters.waon import WaonZaimRowConverterFactory
from zaimcsvconverter.rowconverters.view_card import ViewCardZaimRowConverterFactory
from zaimcsvconverter.rowconverters import ZaimRowConverterFactory
from zaimcsvconverter.zaim_row import ZaimRow, ZaimRowFactory


class FileNameCsvConvert(Enum):
    """This class implements file name of CSV file for convert table data."""
    WAON = 'waon.csv'
    GOLD_POINT_CARD_PLUS = 'gold_point_card_plus.csv'
    MUFG = 'mufg.csv'
    PASMO = 'sf_card_viewer.csv'
    AMAZON = 'amazon.csv'
    VIEW_CARD = 'view_card.csv'
    SUICA = 'sf_card_viewer.csv'

    @property
    def value(self) -> str:
        """This method overwrite super method for type hint."""
        return super().value


@dataclass
class AccountContext(Generic[TypeVarInputRowData, TypeVarInputRow]):
    """This class implements recipe for converting steps for WAON CSV."""
    CSV_FACTORY_SF_CARD_VIEWER = CsvWithHeaderFactory(
        ['利用年月日', '定期', '鉄道会社名', '入場駅/事業者名', '定期', '鉄道会社名', '出場駅/降車場所', '利用額(円)', '残額(円)', 'メモ'], 'shift_jis_2004'
    )
    CSV_FACTORY_AMAZON = CsvWithHeaderFactory(
        [
            '注文日', '注文番号', '商品名', '付帯情報', '価格', '個数', '商品小計', '注文合計',
            'お届け先', '状態', '請求先', '請求額', 'クレカ請求日', 'クレカ請求額', 'クレカ種類',
            '注文概要URL', '領収書URL', '商品URL'
        ],
        'utf-8-sig'
    )
    # Reason: "id" is suitable word and "identity" will cause confuse. pylint: disable=invalid-name
    id: AccountId
    file_name_csv_convert: FileNameCsvConvert
    regex_csv_file_name: str
    csv_factory: CsvFactory
    convert_table_type: ConvertTableType
    input_row_data_class: Type[TypeVarInputRowData]
    input_row_factory: InputRowFactory[TypeVarInputRowData, TypeVarInputRow]
    zaim_row_converter_selector: ZaimRowConverterFactory[TypeVarInputRow]

    def create_convert_table_row_instance(
            self, list_convert_table_row_standard_type_value: List[Any]
    ) -> ConvertTableRecordMixin:
        """This method creates convert table row model instance by list data of convert table row."""
        convert_table_type = self.convert_table_type.value
        return convert_table_type.model(
            self.id, convert_table_type.row_data(*list_convert_table_row_standard_type_value)
        )

    def create_input_row_data_instance(self, list_input_row_standard_type_value: List[str]) -> InputRowData:
        """This method creates input row data instance by list data of input row."""
        # noinspection PyArgumentList
        return self.input_row_data_class(*list_input_row_standard_type_value)  # type: ignore

    def create_input_row_instance(self, input_row_data: TypeVarInputRowData) -> TypeVarInputRow:
        """This method creates input row instance by input row data instance."""
        return self.input_row_factory.create(self.id, input_row_data)

    def convert_input_row_to_zaim_row(self, input_row: TypeVarInputRow) -> ZaimRow:
        """This method converts imput row into zaim row."""
        converter = self.zaim_row_converter_selector.create(input_row)
        return ZaimRowFactory.create(converter)


class Account(Enum):
    """This class implements constant of account in Zaim."""
    WAON = AccountContext(
        AccountId.WAON,
        FileNameCsvConvert.WAON,
        r'.*waon.*\.csv',
        CsvWithHeaderFactory(['取引年月日', '利用店舗', '利用金額（税込）', '利用区分', 'チャージ区分']),
        ConvertTableType.STORE,
        WaonRowData,
        WaonRowFactory(),
        WaonZaimRowConverterFactory(),
    )
    GOLD_POINT_CARD_PLUS = AccountContext(
        AccountId.GOLD_POINT_CARD_PLUS,
        FileNameCsvConvert.GOLD_POINT_CARD_PLUS,
        r'.*gold_point_card_plus.*\.csv',
        CsvFactory('shift_jis_2004'),
        ConvertTableType.STORE,
        GoldPointCardPlusRowData,
        GoldPointCardPlusRowFactory(),
        GoldPointCardPlusZaimRowConverterFactory(),
    )
    GOLD_POINT_CARD_PLUS_201912 = AccountContext(
        AccountId.GOLD_POINT_CARD_PLUS,
        FileNameCsvConvert.GOLD_POINT_CARD_PLUS,
        r'.*gold_point_card_plus_201912.*\.csv',
        CsvWithHeaderFactory(
            [r'.*　様', r'[0-9\*]{4}-[0-9\*]{4}-[0-9\*]{4}-[0-9\*]{4}', 'ゴールドポイントカードプラス'], 'shift_jis_2004'
        ),
        ConvertTableType.STORE,
        GoldPointCardPlus201912RowData,
        GoldPointCardPlus201912RowFactory(),
        GoldPointCardPlus201912ZaimRowConverterFactory(),
    )
    MUFG = AccountContext(
        AccountId.MUFG,
        FileNameCsvConvert.MUFG,
        r'.*mufg.*\.csv',
        CsvWithHeaderFactory(
            ['日付', '摘要', '摘要内容', '支払い金額', '預かり金額', '差引残高', 'メモ', '未資金化区分', '入払区分'], 'shift_jis_2004'
        ),
        ConvertTableType.STORE,
        MufgRowData,
        MufgRowFactory(),
        MufgZaimRowConverterFactory(),
    )
    PASMO = AccountContext(
        AccountId.PASMO,
        FileNameCsvConvert.PASMO,
        r'.*pasmo.*\.csv',
        AccountContext.CSV_FACTORY_SF_CARD_VIEWER,
        ConvertTableType.STORE,
        SFCardViewerRowData,
        # On this timing, CONFIG is not loaded. So we wrap CONFIG by lambda.
        SFCardViewerRowFactory(lambda: CONFIG.pasmo),
        SFCardViewerZaimRowConverterFactory(lambda: CONFIG.pasmo),
    )
    AMAZON = AccountContext(
        AccountId.AMAZON,
        FileNameCsvConvert.AMAZON,
        r'.*amazon.*\.csv',
        AccountContext.CSV_FACTORY_AMAZON,
        ConvertTableType.ITEM,
        AmazonRowData,
        AmazonRowFactory(),
        AmazonZaimRowConverterFactory(),
    )
    AMAZON_201911 = AccountContext(
        AccountId.AMAZON,
        FileNameCsvConvert.AMAZON,
        r'.*amazon_201911.*\.csv',
        AccountContext.CSV_FACTORY_AMAZON,
        ConvertTableType.ITEM,
        Amazon201911RowData,
        Amazon201911RowFactory(),
        Amazon201911ZaimRowConverterFactory(),
    )
    VIEW_CARD = AccountContext(
        AccountId.VIEW_CARD,
        FileNameCsvConvert.VIEW_CARD,
        r'.*view_card.*\.csv',
        ViewCardCsvFactory(),
        ConvertTableType.STORE,
        ViewCardRowData,
        ViewCardRowFactory(),
        ViewCardZaimRowConverterFactory(),
    )
    SUICA = AccountContext(
        AccountId.SUICA,
        FileNameCsvConvert.SUICA,
        r'.*suica.*\.csv',
        AccountContext.CSV_FACTORY_SF_CARD_VIEWER,
        ConvertTableType.STORE,
        SFCardViewerRowData,
        # On this timing, CONFIG is not loaded. So we wrap CONFIG by lambda.
        SFCardViewerRowFactory(lambda: CONFIG.suica),
        SFCardViewerZaimRowConverterFactory(lambda: CONFIG.suica),
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
        matches = [account for account in Account if re.search(account.value.regex_csv_file_name, path.name)]
        if not matches:
            raise ValueError("can't detect account type by csv file name. Please confirm csv file name.")
        return max(matches, key=lambda matched_account: len(matched_account.value.regex_csv_file_name))

    def create_convert_table_row_instance(
            self, list_convert_table_row_standard_type_value: List[Any]
    ) -> ConvertTableRecordMixin:
        """This method creates convert table row model instance by list data of convert table row."""
        return self.value.create_convert_table_row_instance(list_convert_table_row_standard_type_value)

    def create_input_row_data_instance(self, list_input_row_standard_type_value: List[str]) -> InputRowData:
        """This method creates input row data instance by list data of input row."""
        return self.value.create_input_row_data_instance(list_input_row_standard_type_value)

    def create_input_row_instance(self, input_row_data: InputRowData) -> InputRow:
        """This method creates input row instance by input row data instance."""
        return self.value.create_input_row_instance(input_row_data)

    def convert_input_row_to_zaim_row(self, input_row: InputRow) -> ZaimRow:
        """This method converts input row into zaim row."""
        return self.value.convert_input_row_to_zaim_row(input_row)
