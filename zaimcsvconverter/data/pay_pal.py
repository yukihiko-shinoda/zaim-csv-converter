"""PayPal CSV Data model."""
from dataclasses import field
from enum import Enum
from typing import ClassVar

from pydantic.dataclasses import dataclass

from zaimcsvconverter.customdatatypes.string_to_datetime import StringSlashToDateTime
from zaimcsvconverter.first_form_normalizer import CsvRowData


class Status(str, Enum):
    """This class implements constant of status in PayPal CSV."""

    COMPLETED = "完了"
    PENDING = "保留中"
    # DENIED
    # REVERSED
    # ACTIVE
    # EXPIRED
    # REMOVED
    # UNVERIFIED
    # VOIDED
    # PROCESSING
    # CREATED
    # CANCELED


class BalanceImpact(str, Enum):
    """This class implements constant of balance impact in PayPal CSV."""

    CREDIT = "入金"
    DEBIT = "引落し"
    MEMO = "備考"


class TIMEZONE(str, Enum):
    JST = "JST"


class CURRENCY(str, Enum):
    JPY = "JPY"


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods,too-many-instance-attributes
class PayPalRowData(CsvRowData):
    """This class implements data class for wrapping list of PayPal CSV row model."""

    date_: StringSlashToDateTime
    time: str
    time_zone: TIMEZONE
    name: str
    type: str
    status: Status
    currency: CURRENCY
    gross: int
    fee: int
    net: int
    from_email_address: str
    to_email_address: str
    transaction_id: str
    shipping_address: str
    address_status: str
    item_title: str
    item_id: str
    shipping_and_handling_amount: str
    insurance_amount: str
    sales_tax: str
    option_1_name: str
    option_1_value: str
    option_2_name: str
    option_2_value: str
    reference_transaction_id: str
    invoice_number: str
    custom_number: str
    quantity: str
    receipt_id: str
    balance: str
    address_line_1: str
    address_line_2_district_neighborhood: str
    town_city: str
    state_province_region_county_territory_prefecture_republic: str
    zip_postal_code: str
    country: str
    contract_phone_number: str
    subject: str
    note: str
    country_code: str
    balance_impact: BalanceImpact

    HEADER: ClassVar[list[str]] = field(
        default=[
            "日付",
            "時間",
            "タイムゾーン",
            "名前",
            "タイプ",
            "ステータス",
            "通貨",
            "合計",
            "手数料",
            "正味",
            "送信者メールアドレス",
            "受信者メールアドレス",
            "取引ID",
            "配送先住所",
            "住所ステータス",
            "商品タイトル",
            "商品ID",
            "配送および手数料の額",
            "保険金額",
            "消費税",
            "オプション1: 名前",
            "オプション1: 金額",
            "オプション2: 名前",
            "オプション2: 金額",
            "リファレンス トランザクションID",
            "請求書番号",
            "カスタム番号",
            "数量",
            "領収書ID",
            "残高",
            "住所1行目",
            "住所2行目/地区/地域",
            "市区町村",
            "都道府県",
            "郵便番号",
            "国および地域",
            "連絡先の電話番号",
            "件名",
            "備考",
            "国コード",
            "残高への影響",
        ],
        init=False,
    )
