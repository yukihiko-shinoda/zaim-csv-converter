"""This module implements constants which suitable module to belong is not defined."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import re
from types import DynamicClassAttribute
from typing import cast, Generic, List, Type

from godslayer.god_slayer_factory import GodSlayerFactory
from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats import (
    InputRow,
    InputRowData,
    InputRowFactory,
    TypeVarInputRow,
    TypeVarInputRowData,
)
from zaimcsvconverter.inputcsvformats.amazon import AmazonRowData, AmazonRowFactory
from zaimcsvconverter.inputcsvformats.amazon_201911 import Amazon201911RowData, Amazon201911RowFactory
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRowData, GoldPointCardPlusRowFactory
from zaimcsvconverter.inputcsvformats.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912RowData,
    GoldPointCardPlus201912RowFactory,
)
from zaimcsvconverter.inputcsvformats.mufg import MufgRowData, MufgRowFactory
from zaimcsvconverter.inputcsvformats.pay_pal import PayPalRowData, PayPalRowFactory
from zaimcsvconverter.inputcsvformats.sbi_sumishin_net_bank import (
    SBISumishinNetBankRowData,
    SBISumishinNetBankRowFactory,
)
from zaimcsvconverter.inputcsvformats.sf_card_viewer import SFCardViewerRowData, SFCardViewerRowFactory
from zaimcsvconverter.inputcsvformats.view_card import ViewCardRowData, ViewCardRowFactory
from zaimcsvconverter.inputcsvformats.waon import WaonRowData, WaonRowFactory
from zaimcsvconverter.rowconverters.amazon import AmazonZaimRowConverterFactory
from zaimcsvconverter.rowconverters.amazon_201911 import Amazon201911ZaimRowConverterFactory
from zaimcsvconverter.rowconverters.gold_point_card_plus import GoldPointCardPlusZaimRowConverterFactory
from zaimcsvconverter.rowconverters.gold_point_card_plus_201912 import GoldPointCardPlus201912ZaimRowConverterFactory
from zaimcsvconverter.rowconverters.mufg import MufgZaimRowConverterFactory
from zaimcsvconverter.rowconverters.pay_pal import PayPalZaimRowConverterFactory
from zaimcsvconverter.rowconverters.sbi_sumishin_net_bank import SBISumishinNetBankZaimRowConverterFactory
from zaimcsvconverter.rowconverters.sf_card_viewer import SFCardViewerZaimRowConverterFactory
from zaimcsvconverter.rowconverters.view_card import ViewCardZaimRowConverterFactory
from zaimcsvconverter.rowconverters.waon import WaonZaimRowConverterFactory
from zaimcsvconverter.rowconverters import ZaimRowConverterFactory
from zaimcsvconverter.zaim.zaim_row import ZaimRow, ZaimRowFactory


@dataclass
# pylint: disable=too-many-instance-attributes
class AccountContext(Generic[TypeVarInputRowData, TypeVarInputRow]):
    """This class implements recipe for converting steps for WAON CSV."""

    # pylint: disable=invalid-name
    GOD_SLAYER_FACTORY_SF_CARD_VIEWER: GodSlayerFactory = field(
        default=GodSlayerFactory(
            header=["利用年月日", "定期", "鉄道会社名", "入場駅/事業者名", "定期", "鉄道会社名", "出場駅/降車場所", "利用額(円)", "残額(円)", "メモ"],
            encoding="shift_jis_2004",
        ),
        init=False,
    )
    # pylint: disable=invalid-name
    GOD_SLAYER_FACTORY_AMAZON: GodSlayerFactory = field(
        default=GodSlayerFactory(
            header=[
                "注文日",
                "注文番号",
                "商品名",
                "付帯情報",
                "価格",
                "個数",
                "商品小計",
                "注文合計",
                "お届け先",
                "状態",
                "請求先",
                "請求額",
                "クレカ請求日",
                "クレカ請求額",
                "クレカ種類",
                "注文概要URL",
                "領収書URL",
                "商品URL",
            ],
            partition=[
                r"\d{4}/\d{1,2}/\d{1,2}",
                r".*",
                "（注文全体）",
                "",
                "",
                "",
                "",
                r"\d*",
                "",
                "",
                r".*",
                r"\d*",
                "",
                "",
                r".*",
                r".*",
                r".*",
                "",
            ],
            encoding="utf-8-sig",
        ),
        init=False,
    )
    regex_csv_file_name: str
    god_slayer_factory: GodSlayerFactory
    input_row_data_class: Type[TypeVarInputRowData]
    input_row_factory: InputRowFactory[TypeVarInputRowData, TypeVarInputRow]
    zaim_row_converter_factory: ZaimRowConverterFactory[TypeVarInputRow, TypeVarInputRowData]

    def create_input_row_data_instance(self, list_input_row_standard_type_value: List[str]) -> InputRowData:
        """This method creates input row data instance by list data of input row."""
        # noinspection PyArgumentList
        return self.input_row_data_class(*list_input_row_standard_type_value)

    def create_input_row_instance(
        self, input_row_data: TypeVarInputRowData
    ) -> Kind1[TypeVarInputRow, TypeVarInputRowData]:
        """This method creates input row instance by input row data instance."""
        return self.input_row_factory.create(input_row_data)

    def convert_input_row_to_zaim_row(self, input_row: Kind1[TypeVarInputRow, TypeVarInputRowData]) -> ZaimRow:
        """This method converts input row into zaim row."""
        converter = self.zaim_row_converter_factory.create(input_row)
        return ZaimRowFactory.create(converter)


class Account(Enum):
    """This class implements constant of account in Zaim."""

    WAON = AccountContext(
        r".*waon.*\.csv",
        GodSlayerFactory(header=["取引年月日", "利用店舗", "利用金額（税込）", "利用区分", "チャージ区分"]),
        WaonRowData,
        WaonRowFactory(),
        WaonZaimRowConverterFactory(),
    )
    GOLD_POINT_CARD_PLUS = AccountContext(
        r".*gold_point_card_plus.*\.csv",
        GodSlayerFactory(encoding="shift_jis_2004"),
        GoldPointCardPlusRowData,
        GoldPointCardPlusRowFactory(),
        GoldPointCardPlusZaimRowConverterFactory(),
    )
    GOLD_POINT_CARD_PLUS_201912 = AccountContext(
        r".*gold_point_card_plus_201912.*\.csv",
        GodSlayerFactory(
            header=[r".*　様", r"[0-9\*]{4}-[0-9\*]{4}-[0-9\*]{4}-[0-9\*]{4}", "ゴールドポイントカードプラス"],
            footer=["^$", "^$", "^$", "^$", "^$", r"^\d*$", "^$"],
            encoding="shift_jis_2004",
        ),
        GoldPointCardPlus201912RowData,
        GoldPointCardPlus201912RowFactory(),
        GoldPointCardPlus201912ZaimRowConverterFactory(),
    )
    GOLD_POINT_CARD_PLUS_202009 = AccountContext(
        r".*gold_point_card_plus_202009.*\.csv",
        GodSlayerFactory(
            header=[r".*　様", r"[0-9\*]{4}-[0-9\*]{4}-[0-9\*]{4}-[0-9\*]{4}", "ゴールドポイントカードプラス", "", "", "", ""],
            footer=["^$", "^$", "^$", "^$", "^$", r"^\d*$", "^$"],
            encoding="shift_jis_2004",
        ),
        GoldPointCardPlus201912RowData,
        GoldPointCardPlus201912RowFactory(),
        GoldPointCardPlus201912ZaimRowConverterFactory(),
    )
    MUFG = AccountContext(
        r".*mufg.*\.csv",
        GodSlayerFactory(
            header=["日付", "摘要", "摘要内容", "支払い金額", "預かり金額", "差引残高", "メモ", "未資金化区分", "入払区分"], encoding="shift_jis_2004",
        ),
        MufgRowData,
        MufgRowFactory(),
        MufgZaimRowConverterFactory(),
    )
    PASMO = AccountContext(
        r".*pasmo.*\.csv",
        AccountContext.GOD_SLAYER_FACTORY_SF_CARD_VIEWER,
        SFCardViewerRowData,
        # On this timing, CONFIG is not loaded. So we wrap CONFIG by lambda.
        SFCardViewerRowFactory(lambda: CONFIG.pasmo),
        SFCardViewerZaimRowConverterFactory(lambda: CONFIG.pasmo),
    )
    AMAZON = AccountContext(
        r".*amazon.*\.csv",
        AccountContext.GOD_SLAYER_FACTORY_AMAZON,
        AmazonRowData,
        AmazonRowFactory(),
        AmazonZaimRowConverterFactory(),
    )
    AMAZON_201911 = AccountContext(
        r".*amazon_201911.*\.csv",
        AccountContext.GOD_SLAYER_FACTORY_AMAZON,
        Amazon201911RowData,
        Amazon201911RowFactory(),
        Amazon201911ZaimRowConverterFactory(),
    )
    VIEW_CARD = AccountContext(
        r".*view_card.*\.csv",
        GodSlayerFactory(
            header=[
                "ご利用年月日",
                "ご利用箇所",
                "ご利用額",
                "払戻額",
                "ご請求額（うち手数料・利息）",
                "支払区分（回数）",
                "今回回数",
                "今回ご請求額・弁済金（うち手数料・利息）",
                "現地通貨額",
                "通貨略称",
                "換算レート",
            ],
            partition=[r"^\*{4}-\*{4}-\*{4}-[0-9]{4}\s.*$"],
            encoding="shift_jis_2004",
        ),
        ViewCardRowData,
        ViewCardRowFactory(),
        ViewCardZaimRowConverterFactory(),
    )
    SUICA = AccountContext(
        r".*suica.*\.csv",
        AccountContext.GOD_SLAYER_FACTORY_SF_CARD_VIEWER,
        SFCardViewerRowData,
        # On this timing, CONFIG is not loaded. So we wrap CONFIG by lambda.
        SFCardViewerRowFactory(lambda: CONFIG.suica),
        SFCardViewerZaimRowConverterFactory(lambda: CONFIG.suica),
    )
    PAY_PAL = AccountContext(
        r".*pay_pal.*\.csv",
        GodSlayerFactory(header=PayPalRowData.HEADER),
        PayPalRowData,
        PayPalRowFactory(),
        PayPalZaimRowConverterFactory(),
    )
    SBI_SUMISHIN_NET_BANK = AccountContext(
        r".*sbi_sumishin_net_bank.*\.csv",
        GodSlayerFactory(header=["日付", "内容", "出金金額(円)", "入金金額(円)", "残高(円)", "メモ"], encoding="shift_jis_2004",),
        SBISumishinNetBankRowData,
        SBISumishinNetBankRowFactory(),
        SBISumishinNetBankZaimRowConverterFactory(),
    )

    @DynamicClassAttribute
    def value(self) -> AccountContext[InputRowData, InputRow[InputRowData]]:
        """This method overwrite super method for type hint."""
        return cast(AccountContext[InputRowData, InputRow[InputRowData]], super().value)

    @staticmethod
    def create_by_path_csv_input(path: Path) -> Account:
        """This function create correct setting instance by argument."""
        # noinspection PyUnusedLocal
        matches = [account for account in Account if re.search(account.value.regex_csv_file_name, path.name)]
        if not matches:
            raise ValueError("can't detect account type by csv file name. Please confirm csv file name.")
        return max(matches, key=lambda matched_account: len(matched_account.value.regex_csv_file_name))
