"""This module implements row model of WAON CSV."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

from zaimcsvconverter.inputcsvformats import InputStoreRowData, InputStoreRow, InputRowFactory
from zaimcsvconverter.models import AccountId
from zaimcsvconverter.utility import Utility


@dataclass
class WaonRowData(InputStoreRowData):
    """This class implements data class for wrapping list of WAON CSV row model."""
    class UseKind(Enum):
        """This class implements constant of user kind in WAON CSV."""
        PAYMENT = '支払'
        CHARGE = 'チャージ'
        AUTO_CHARGE = 'オートチャージ'
        DOWNLOAD_POINT = 'ポイントダウンロード'

    class ChargeKind(Enum):
        """This class implements constant of charge kind in WAON CSV."""
        BANK_ACCOUNT = '銀行口座'
        POINT = 'ポイント'
        CASH = '現金'
        NULL = '-'

    _date: str
    _used_store: str
    _used_amount: str
    _use_kind: str
    _charge_kind: str

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        return self._used_store

    @property
    def used_amount(self) -> int:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return Utility.convert_yen_string_to_int(self._used_amount)

    @property
    def use_kind(self) -> WaonRowData.UseKind:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.UseKind(self._use_kind)

    @property
    def charge_kind(self) -> WaonRowData.ChargeKind:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.ChargeKind(self._charge_kind)

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.date,
            f'Invalid date. Date = {self._date}'
        )
        self.stock_error(
            lambda: self.used_amount,
            f'Invalid used amount. Used amount = {self._used_amount}'
        )
        self.stock_error(
            lambda: self.use_kind,
            f'Invalid used amount. Use kind = {self._use_kind}'
        )
        self.stock_error(
            lambda: self.charge_kind,
            f'The value of "Charge kind" has not been defined in this code. Charge kind = {self._charge_kind}'
        )
        return super().validate


class WaonRow(InputStoreRow):
    """This class implements row model of WAON CSV."""
    def __init__(self, account_id: AccountId, row_data: WaonRowData):
        super().__init__(account_id, row_data)
        self.used_amount: int = row_data.used_amount
        self.use_kind: WaonRowData.UseKind = row_data.use_kind

    @property
    def is_row_to_skip(self) -> bool:
        """This property returns whether this row should be skipped or not."""
        return self.is_download_point

    @property
    def is_payment(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.use_kind == WaonRowData.UseKind.PAYMENT

    @property
    def is_charge(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.use_kind == WaonRowData.UseKind.CHARGE

    @property
    def is_auto_charge(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.use_kind == WaonRowData.UseKind.AUTO_CHARGE

    @property
    def is_download_point(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.use_kind == WaonRowData.UseKind.DOWNLOAD_POINT


class WaonChargeRow(WaonRow):
    """This class implements charge row model of WAON CSV."""
    def __init__(self, account_id: AccountId, row_data: WaonRowData):
        super().__init__(account_id, row_data)
        self._charge_kind: WaonRowData.ChargeKind = row_data.charge_kind

    @property
    def charge_kind(self):
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        if self._charge_kind == WaonRowData.ChargeKind.NULL:
            raise ValueError(f'Charge kind on charge row is not allowed "{WaonRowData.ChargeKind.NULL.value}".')
        return self._charge_kind

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.charge_kind,
            f'Charge kind in charge row is required. Charge kind = {self._charge_kind}'
        )
        return super().validate

    @property
    def is_charge_by_point(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.is_charge and self.charge_kind == WaonRowData.ChargeKind.POINT

    @property
    def is_charge_by_cash(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.is_charge and self.charge_kind == WaonRowData.ChargeKind.CASH

    @property
    def is_charge_by_bank_account(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.is_charge and self.charge_kind == WaonRowData.ChargeKind.BANK_ACCOUNT


class WaonRowFactory(InputRowFactory[WaonRowData, WaonRow]):
    """This class implements factory to create WAON CSV row instance."""
    def create(self, account_id: AccountId, input_row_data: WaonRowData) -> WaonRow:
        if input_row_data.use_kind in (WaonRowData.UseKind.CHARGE, WaonRowData.UseKind.AUTO_CHARGE):
            return WaonChargeRow(account_id, input_row_data)
        return WaonRow(account_id, input_row_data)
