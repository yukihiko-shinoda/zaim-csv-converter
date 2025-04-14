"""This module implements Zaim CSV format."""

# Reason: Guarding for the future when it comes to calculating constants
# pylint: disable=too-few-public-methods
from typing import ClassVar


class ZaimCsvFormat:
    """This class implements Zaim CSV format."""

    HEADER: ClassVar[list[str]] = [
        "日付",
        "方法",
        "カテゴリ",
        "カテゴリの内訳",
        "支払元",
        "入金先",
        "品目",
        "メモ",
        "お店",
        "通貨",
        "収入",
        "支出",
        "振替",
        "残高調整",
        "通貨変換前の金額",
        "集計の設定",
    ]
    CATEGORY_LARGE_EMPTY = ""
    CATEGORY_SMALL_EMPTY = ""
    CATEGORY_LARGE_NOT_USE = "-"
    CATEGORY_SMALL_NOT_USE = "-"
    CASH_FLOW_SOURCE_EMPTY = ""
    CASH_FLOW_TARGET_EMPTY = ""
    AMOUNT_INCOME_EMPTY = 0
    AMOUNT_PAYMENT_EMPTY = 0
    AMOUNT_TRANSFER_EMPTY = 0
    STORE_NAME_EMPTY = ""
    ITEM_NAME_EMPTY = ""
    NOTE_EMPTY = ""
    CURRENCY_EMPTY = ""
    BALANCE_ADJUSTMENT_EMPTY = ""
    AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY = ""
    SETTING_AGGREGATE_EMPTY = ""
