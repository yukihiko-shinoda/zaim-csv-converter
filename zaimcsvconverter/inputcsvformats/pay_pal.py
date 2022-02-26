"""This module implements row model of PayPal CSV.

see:
  - PayPal activity download specification
    https://www.paypalobjects.com/webstatic/en_US/developer/docs/pdf/PP_ActivityDownload.pdf
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import ClassVar, List

from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats import InputRowFactory, InputStoreItemRow, InputStoreItemRowData


@dataclass
# Reason: Specification. pylint: disable=too-many-instance-attributes
class PayPalRowData(InputStoreItemRowData):
    """This class implements data class for wrapping list of PayPal CSV row model."""

    HEADER: ClassVar[List[str]] = field(
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

    class Status(Enum):
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

    class BalanceImpact(Enum):
        """This class implements constant of balance impact in PayPal CSV."""

        CREDIT = "入金"
        DEBIT = "引落し"
        MEMO = "備考"

    _date: str
    time: str
    _time_zone: str
    _name: str
    type: str
    _status: str
    _currency: str
    _gross: str
    _fee: str
    _net: str
    from_email_address: str
    to_email_address: str
    transaction_id: str
    shipping_address: str
    address_status: str
    _item_title: str
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
    _balance_impact: str

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._date, "%Y/%m/%d")

    @property
    def time_zone(self) -> str:
        if self._time_zone != "JST":
            raise ValueError()
        return self._time_zone

    @property
    def store_name(self) -> str:
        return self._name

    @property
    def item_name(self) -> str:
        return self._item_title

    @property
    def status(self) -> PayPalRowData.Status:
        return self.Status(self._status)

    @property
    def currency(self) -> str:
        if self._currency != "JPY":
            raise ValueError()
        return self._currency

    @property
    def gross(self) -> int:
        return int(self._gross)

    @property
    def fee(self) -> int:
        return int(self._fee)

    @property
    def net(self) -> int:
        return int(self._net)

    @property
    def balance_impact(self) -> PayPalRowData.BalanceImpact:
        return self.BalanceImpact(self._balance_impact)

    @property
    def validate(self) -> bool:
        self.stock_error(lambda: self.date, f"Invalid date. Date = {self._date}")
        self.stock_error(lambda: self.time_zone, f"Only JST is supported. Time zone = {self.time_zone}")
        self.stock_error(lambda: self.status, f"Invalid status. Status = {self._status}")
        self.stock_error(lambda: self.currency, f"Invalid currency. Currency = {self._currency}")
        self.stock_error(
            lambda: self.balance_impact, f"Invalid balance impact. Balance impact = {self._balance_impact}"
        )
        return super().validate

    def create_pydantic(self) -> None:
        return None


class PayPalRow(InputStoreItemRow[PayPalRowData]):
    """This class implements row model of Amazon.co.jp CSV."""

    def __init__(self, row_data: PayPalRowData):
        super().__init__(row_data, FileCsvConvert.PAY_PAL_STORE.value, FileCsvConvert.PAY_PAL_ITEM.value)
        self.status: PayPalRowData.Status = row_data.status
        self.gross: int = row_data.gross
        self.fee: int = row_data.fee
        self.net: int = row_data.net
        self.balance_impact: PayPalRowData.BalanceImpact = row_data.balance_impact

    @property
    def validate(self) -> bool:
        self.stock_error(
            self.check_net_is_gross_plus_fee,
            f"Net is not gross + fee. Net: {self.net}, gross: {self.gross}, fee: {self.fee}",
        )
        return super().validate

    def check_net_is_gross_plus_fee(self) -> None:
        if self.net != self.gross + self.fee:
            raise ValueError()

    @property
    def is_row_to_skip(self) -> bool:
        return not self.is_completed or self.is_debit or self.is_memo

    @property
    def is_completed(self) -> bool:
        return self.status == PayPalRowData.Status.COMPLETED

    @property
    def is_debit(self) -> bool:
        return self.balance_impact == PayPalRowData.BalanceImpact.DEBIT

    @property
    def is_memo(self) -> bool:
        return self.balance_impact == PayPalRowData.BalanceImpact.MEMO


class PayPalRowFactory(InputRowFactory[PayPalRowData, PayPalRow]):
    """This class implements factory to create Amazon.co.jp CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: PayPalRowData) -> PayPalRow:  # type: ignore
        return PayPalRow(input_row_data)
