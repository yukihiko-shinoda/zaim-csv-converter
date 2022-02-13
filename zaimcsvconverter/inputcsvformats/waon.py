"""This module implements row model of WAON CSV."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats import InputRowFactory, InputStoreRow, InputStoreRowData
from zaimcsvconverter.utility import Utility


@dataclass
class WaonRowData(InputStoreRowData):
    """This class implements data class for wrapping list of WAON CSV row model."""

    class UseKind(Enum):
        """This class implements constant of user kind in WAON CSV."""

        PAYMENT = "支払"
        PAYMENT_CANCEL = "支払取消"
        CHARGE = "チャージ"
        AUTO_CHARGE = "オートチャージ"
        DOWNLOAD_POINT = "ポイントダウンロード"
        TRANSFER_WAON_UPLOAD = "WAON移行（アップロード）"
        TRANSFER_WAON_DOWNLOAD = "WAON移行（ダウンロード）"

    class ChargeKind(Enum):
        """This class implements constant of charge kind in WAON CSV."""

        BANK_ACCOUNT = "銀行口座"
        POINT = "ポイント"
        CASH = "現金"
        DOWNLOAD_VALUE = "バリューダウンロード"
        NULL = "-"

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
        return Utility.convert_yen_string_to_int(self._used_amount)

    @property
    def use_kind(self) -> WaonRowData.UseKind:
        return self.UseKind(self._use_kind)

    @property
    def charge_kind(self) -> WaonRowData.ChargeKind:
        return self.ChargeKind(self._charge_kind)

    @property
    def validate(self) -> bool:
        self.stock_error(lambda: self.date, f"Invalid date. Date = {self._date}")
        self.stock_error(lambda: self.used_amount, f"Invalid used amount. Used amount = {self._used_amount}")
        self.stock_error(lambda: self.use_kind, f"Invalid used amount. Use kind = {self._use_kind}")
        self.stock_error(
            lambda: self.charge_kind,
            f'The value of "Charge kind" has not been defined in this code. Charge kind = {self._charge_kind}',
        )
        return super().validate


class WaonRow(InputStoreRow[WaonRowData]):
    """This class implements row model of WAON CSV."""

    def __init__(self, row_data: WaonRowData):
        super().__init__(row_data, FileCsvConvert.WAON.value)
        self.used_amount: int = row_data.used_amount
        self.use_kind: WaonRowData.UseKind = row_data.use_kind

    @property
    def is_row_to_skip(self) -> bool:
        """This property returns whether this row should be skipped or not."""
        return self.is_download_point or self.is_transfer_waon_upload or self.is_transfer_waon_download

    @property
    def is_payment(self) -> bool:
        return self.use_kind == WaonRowData.UseKind.PAYMENT

    @property
    def is_payment_cancel(self) -> bool:
        return self.use_kind == WaonRowData.UseKind.PAYMENT_CANCEL

    @property
    def is_charge(self) -> bool:
        return self.use_kind == WaonRowData.UseKind.CHARGE

    @property
    def is_auto_charge(self) -> bool:
        return self.use_kind == WaonRowData.UseKind.AUTO_CHARGE

    @property
    def is_download_point(self) -> bool:
        return self.use_kind == WaonRowData.UseKind.DOWNLOAD_POINT

    @property
    def is_transfer_waon_upload(self) -> bool:
        return self.use_kind == WaonRowData.UseKind.TRANSFER_WAON_UPLOAD

    @property
    def is_transfer_waon_download(self) -> bool:
        return self.use_kind == WaonRowData.UseKind.TRANSFER_WAON_DOWNLOAD


class WaonChargeRow(WaonRow):
    """This class implements charge row model of WAON CSV."""

    def __init__(self, row_data: WaonRowData):
        super().__init__(row_data)
        self._charge_kind: WaonRowData.ChargeKind = row_data.charge_kind

    @property
    def charge_kind(self) -> WaonRowData.ChargeKind:
        if self._charge_kind == WaonRowData.ChargeKind.NULL:
            raise ValueError(f'Charge kind on charge row is not allowed "{WaonRowData.ChargeKind.NULL.value}".')
        return self._charge_kind

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.charge_kind, f"Charge kind in charge row is required. Charge kind = {self._charge_kind}"
        )
        return super().validate

    @property
    def is_charge_by_point(self) -> bool:
        return self.is_charge and self.charge_kind == WaonRowData.ChargeKind.POINT

    @property
    def is_charge_by_cash(self) -> bool:
        return self.is_charge and self.charge_kind == WaonRowData.ChargeKind.CASH

    @property
    def is_charge_by_bank_account(self) -> bool:
        return self.is_charge and self.charge_kind == WaonRowData.ChargeKind.BANK_ACCOUNT

    @property
    def is_charge_by_download_value(self) -> bool:
        return self.is_charge and self.charge_kind == WaonRowData.ChargeKind.DOWNLOAD_VALUE


class WaonRowFactory(InputRowFactory[WaonRowData, WaonRow]):
    """This class implements factory to create WAON CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: WaonRowData) -> WaonRow:  # type: ignore
        if input_row_data.use_kind in (WaonRowData.UseKind.CHARGE, WaonRowData.UseKind.AUTO_CHARGE):
            return WaonChargeRow(input_row_data)
        return WaonRow(input_row_data)
