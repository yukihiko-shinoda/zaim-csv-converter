"""The constants for accounts in Zaim."""

from __future__ import annotations

import re
from enum import Enum
from typing import TYPE_CHECKING

from godslayer.god_slayer_factory import GodSlayerFactory

from zaimcsvconverter import CONFIG
from zaimcsvconverter.accounts.context import AccountContext
from zaimcsvconverter.inputtooutput.converters.recordtozaim.amazon import AmazonZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim.amazon_201911 import Amazon201911ZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim.gold_point_card_plus import (
    GoldPointCardPlusZaimRowConverterFactory,  # noqa: H301,RUF100
)
from zaimcsvconverter.inputtooutput.converters.recordtozaim.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912ZaimRowConverterFactory,  # noqa: H301,RUF100
)
from zaimcsvconverter.inputtooutput.converters.recordtozaim.mobile_suica import MobileSuicaZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim.mufg import MufgZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim.pay_pal import PayPalZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim.pay_pay_card import PayPayCardZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim.sbi_sumishin_net_bank import (
    SBISumishinNetBankZaimRowConverterFactory,  # noqa: H301,RUF100
)
from zaimcsvconverter.inputtooutput.converters.recordtozaim.sf_card_viewer import SFCardViewerZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim.view_card import ViewCardZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim.waon import WaonZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.amazon import AmazonRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.amazon_201911 import Amazon201911RowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.gold_point_card_plus import (
    GoldPointCardPlusRowFactory,  # noqa: H301,RUF100
)
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912RowFactory,  # noqa: H301,RUF100
)
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.mobile_suica import MobileSuicaRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.mufg import MufgRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.pay_pal import PayPalRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.pay_pay_card import PayPayCardRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.sbi_sumishin_net_bank import (
    SBISumishinNetBankRowFactory,  # noqa: H301,RUF100
)
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.sf_card_viewer import SFCardViewerRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.view_card import ViewCardRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.waon import WaonRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.amazon import AmazonRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.amazon_201911 import Amazon201911RowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.gold_point_card_plus import GoldPointCardPlusRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912RowData,  # noqa: H301,RUF100
)
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.mobile_suica import MobileSuicaRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.mufg import MufgRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.pay_pal import PayPalRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.pay_pay_card import PayPayCardRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.sbi_sumishin_net_bank import SBISumishinNetBankRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.sf_card_viewer import SFCardViewerRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.view_card import ViewCardRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.waon import WaonRowData

if TYPE_CHECKING:
    from pathlib import Path


class Account(Enum):
    """This class implements constant of account in Zaim."""

    WAON = AccountContext(
        r".*waon.*\.csv",
        # Reason: Specification.
        GodSlayerFactory(
            header=[
                "取引年月日",
                "利用店舗",
                "利用金額（税込）",  # noqa: RUF001
                "利用区分",
                "チャージ区分",
            ],
        ),
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
    # fmt: off
    GOLD_POINT_CARD_PLUS_202009 = AccountContext(
        r".*gold_point_card_plus_202009.*\.csv",
        GodSlayerFactory(
            header=[
                r".*　様", r"[0-9\*]{4}-[0-9\*]{4}-[0-9\*]{4}-[0-9\*]{4}", "ゴールドポイントカードプラス",
                "", "", "", "",
            ],
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
            header=[
                "日付", "摘要", "摘要内容", "支払い金額", "預かり金額",
                "差引残高", "メモ", "未資金化区分", "入払区分",
            ],
            encoding="shift_jis_2004",
        ),
        MufgRowData,
        MufgRowFactory(),
        MufgZaimRowConverterFactory(),
    )
    # fmt: on
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
                # Reason: Specification.
                "ご請求額（うち手数料・利息）",  # noqa: RUF001
                # Reason: Specification.
                "支払区分（回数）",  # noqa: RUF001
                "今回回数",
                # Reason: Specification.
                "今回ご請求額・弁済金（うち手数料・利息）",  # noqa: RUF001
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
        GodSlayerFactory(
            header=["日付", "内容", "出金金額(円)", "入金金額(円)", "残高(円)", "メモ"],
            encoding="shift_jis_2004",
        ),
        SBISumishinNetBankRowData,
        SBISumishinNetBankRowFactory(),
        SBISumishinNetBankZaimRowConverterFactory(),
    )
    # fmt: off
    PAY_PAY_CARD = AccountContext(
        r".*pay_pay_card.*\.csv",
        GodSlayerFactory(
            header=[
                "利用日/キャンセル日", "利用店名・商品名", "利用者", "支払区分", "利用金額",
                "手数料", "支払総額", "当月支払金額", "翌月以降繰越金額", "調整額", "当月お支払日",
            ],
        ),
        PayPayCardRowData,
        PayPayCardRowFactory(),
        PayPayCardZaimRowConverterFactory(),
    )
    # fmt: on
    MOBILE_SUICA = AccountContext(
        r".*mobile_suica.*\.csv",
        GodSlayerFactory(header=["月日", "種別", "利用場所", "種別", "利用場所", "残高", "入金・利用額"]),
        MobileSuicaRowData,
        # On this timing, CONFIG is not loaded. So we wrap CONFIG by lambda.
        MobileSuicaRowFactory(lambda: CONFIG.suica),
        MobileSuicaZaimRowConverterFactory(lambda: CONFIG.suica),
    )

    @staticmethod
    def create_by_path_csv_input(path: Path) -> Account:
        """This function create correct setting instance by argument."""
        # noinspection PyUnusedLocal
        matches = [account for account in Account if re.search(account.value.regex_csv_file_name, path.name)]
        if not matches:
            msg = f"can't detect account type by csv file name. Please confirm csv file name: {path.name}"
            raise ValueError(msg)
        return max(matches, key=lambda matched_account: len(matched_account.value.regex_csv_file_name))
