"""This module implements row model of WAON CSV."""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic.dataclasses import dataclass

from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.inputcsvformats.customdatatypes.yen_string_to_int import StrictYenStringToInt
from zaimcsvconverter.inputcsvformats import InputStoreRow, InputStoreRowData


class UseKind(str, Enum):
    """This class implements constant of user kind in WAON CSV."""

    PAYMENT = "支払"
    PAYMENT_CANCEL = "支払取消"
    CHARGE = "チャージ"
    AUTO_CHARGE = "オートチャージ"
    DOWNLOAD_POINT = "ポイントダウンロード"
    TRANSFER_WAON_UPLOAD = "WAON移行（アップロード）"
    TRANSFER_WAON_DOWNLOAD = "WAON移行（ダウンロード）"


class ChargeKind(str, Enum):
    """This class implements constant of charge kind in WAON CSV."""

    BANK_ACCOUNT = "銀行口座"
    POINT = "ポイント"
    CASH = "現金"
    DOWNLOAD_VALUE = "バリューダウンロード"
    NULL = "-"


# Reason: Model. pylint: disable=too-few-public-methods
@dataclass
class WaonRowData(InputStoreRowData):
    """This class implements data class for wrapping list of WAON CSV row model."""

    date_: StringToDateTime
    used_store: str
    used_amount: StrictYenStringToInt
    use_kind: UseKind
    charge_kind: ChargeKind

    @property
    def date(self) -> datetime:
        return self.date_

    @property
    def store_name(self) -> str:
        return self.used_store


class WaonRow(InputStoreRow[WaonRowData]):
    """This class implements row model of WAON CSV."""

    def __init__(self, row_data: WaonRowData):
        super().__init__(row_data, FileCsvConvert.WAON.value)
        self.used_amount: int = row_data.used_amount
        self.use_kind: UseKind = row_data.use_kind

    @property
    def is_row_to_skip(self) -> bool:
        """This property returns whether this row should be skipped or not."""
        return self.is_download_point or self.is_transfer_waon_upload or self.is_transfer_waon_download

    @property
    def is_payment(self) -> bool:
        return self.use_kind == UseKind.PAYMENT

    @property
    def is_payment_cancel(self) -> bool:
        return self.use_kind == UseKind.PAYMENT_CANCEL

    @property
    def is_charge(self) -> bool:
        return self.use_kind == UseKind.CHARGE

    @property
    def is_auto_charge(self) -> bool:
        return self.use_kind == UseKind.AUTO_CHARGE

    @property
    def is_download_point(self) -> bool:
        return self.use_kind == UseKind.DOWNLOAD_POINT

    @property
    def is_transfer_waon_upload(self) -> bool:
        return self.use_kind == UseKind.TRANSFER_WAON_UPLOAD

    @property
    def is_transfer_waon_download(self) -> bool:
        return self.use_kind == UseKind.TRANSFER_WAON_DOWNLOAD


class WaonChargeRow(WaonRow):
    """This class implements charge row model of WAON CSV."""

    def __init__(self, row_data: WaonRowData):
        super().__init__(row_data)
        self._charge_kind: ChargeKind = row_data.charge_kind

    @property
    def charge_kind(self) -> ChargeKind:
        if self._charge_kind == ChargeKind.NULL:
            raise ValueError(f'Charge kind on charge row is not allowed "{ChargeKind.NULL.value}".')
        return self._charge_kind

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.charge_kind, f"Charge kind in charge row is required. Charge kind = {self._charge_kind}"
        )
        return super().validate

    @property
    def is_charge_by_point(self) -> bool:
        return self.is_charge and self.charge_kind == ChargeKind.POINT

    @property
    def is_charge_by_cash(self) -> bool:
        return self.is_charge and self.charge_kind == ChargeKind.CASH

    @property
    def is_charge_by_bank_account(self) -> bool:
        return self.is_charge and self.charge_kind == ChargeKind.BANK_ACCOUNT

    @property
    def is_charge_by_download_value(self) -> bool:
        return self.is_charge and self.charge_kind == ChargeKind.DOWNLOAD_VALUE
