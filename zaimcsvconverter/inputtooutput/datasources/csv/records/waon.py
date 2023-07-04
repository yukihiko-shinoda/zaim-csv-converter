"""This module implements row model of WAON CSV."""
from __future__ import annotations

from zaimcsvconverter.data.waon import ChargeKind, UseKind
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csv.data.waon import WaonRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputRow, InputStoreRow


class WaonRowToSkip(InputRow[WaonRowData]):
    @property
    def is_row_to_skip(self) -> bool:
        return True


class WaonRow(InputStoreRow[WaonRowData]):
    """This class implements row model of WAON CSV."""

    def __init__(self, row_data: WaonRowData) -> None:
        super().__init__(row_data, FileCsvConvert.WAON.value)
        self.used_amount: int = row_data.used_amount
        self.use_kind: UseKind = row_data.use_kind

    @property
    def is_row_to_skip(self) -> bool:
        return False

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


class WaonChargeRow(WaonRow):
    """This class implements charge row model of WAON CSV."""

    def __init__(self, row_data: WaonRowData) -> None:
        super().__init__(row_data)
        self._charge_kind: ChargeKind = row_data.charge_kind

    @property
    def charge_kind(self) -> ChargeKind:
        if self._charge_kind == ChargeKind.NULL:
            msg = f'Charge kind on charge row is not allowed "{ChargeKind.NULL.value}".'
            raise ValueError(msg)
        return self._charge_kind

    @property
    def validate(self) -> bool:
        self.stock_error(
            lambda: self.charge_kind,
            f"Charge kind in charge row is required. Charge kind = {self._charge_kind}",
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
