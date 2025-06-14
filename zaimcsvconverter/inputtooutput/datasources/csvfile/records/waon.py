"""This module implements row model of WAON CSV."""

from __future__ import annotations

from typing import Any

from zaimcsvconverter import CONFIG
from zaimcsvconverter.data.waon import ChargeKind
from zaimcsvconverter.data.waon import UseKind
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.waon import WaonRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import InputRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import InputStoreRow


class WaonRow(InputRow[WaonRowData]):
    """This class implements row model of WAON CSV."""

    def __init__(self, row_data: WaonRowData, *args: Any, **kwargs: Any) -> None:
        super().__init__(row_data, *args, **kwargs)
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


class WaonRowToSkip(WaonRow):
    """This class implements row to skip model of WAON CSV."""

    @property
    def is_row_to_skip(self) -> bool:
        return True


class WaonStoreRow(WaonRow, InputStoreRow[WaonRowData]):
    """This class implements store row model of WAON CSV."""

    def __init__(self, row_data: WaonRowData) -> None:
        super().__init__(row_data, FileCsvConvert.WAON.value)


# Reason: Specification requires. pylint: disable=too-many-ancestors
class WaonChargeRow(WaonStoreRow):
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
    def is_income(self) -> bool:
        return self.is_charge_by_point or self.is_charge_by_download_value

    @property
    def is_transfer(self) -> bool:
        return self.is_auto_charge or self.is_charge_by_bank_account or self.is_charge_by_cash

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

    @property
    def is_row_to_skip(self) -> bool:
        return self.is_transfer_from_auto_charge_source and CONFIG.waon.skip_transfer_from_auto_charge_source_row

    @property
    def is_transfer_from_auto_charge_source(self) -> bool:
        """Check if the row is a transfer from auto charge source."""
        return ChargeKind(CONFIG.waon.auto_charge_source_type) == self.charge_kind
