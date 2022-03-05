"""This module implements convert steps from WAON input row to Zaim row."""
from typing import cast

from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.waon import WaonChargeRow, WaonRow, WaonRowData
from zaimcsvconverter.rowconverters import (
    CsvRecordToZaimRowConverterFactory,
    ZaimIncomeRowStoreConverter,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
    ZaimTransferRowConverter,
)


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class WaonZaimIncomeRowConverter(ZaimIncomeRowStoreConverter[WaonChargeRow, WaonRowData]):
    """This class implements convert steps from WAON input row to Zaim income row."""

    @property
    def cash_flow_target(self) -> str:
        return CONFIG.waon.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class WaonZaimPaymentRowConverter(ZaimPaymentRowStoreConverter[WaonRow, WaonRowData]):
    """This class implements convert steps from WAON input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.waon.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return -self.input_row.used_amount if self.input_row.is_payment_cancel else self.input_row.used_amount


class WaonZaimTransferRowConverter(ZaimTransferRowConverter[WaonRow, WaonRowData]):
    """This class implements convert steps from WAON input row to Zaim transfer row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.waon.auto_charge_source

    @property
    def cash_flow_target(self) -> str:
        return CONFIG.waon.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


class WaonZaimRowConverterFactory(CsvRecordToZaimRowConverterFactory[WaonRow, WaonRowData]):
    """This class implements select steps from WAON input row to Zaim row converter."""

    # Reason: Maybe, there are no way to resolve.
    # The nearest issues: https://github.com/dry-python/returns/issues/708
    def create(self, input_row: Kind1[WaonRow, WaonRowData]) -> ZaimRowConverter[WaonRow, WaonRowData]:  # type: ignore
        if isinstance(input_row, WaonChargeRow) and (
            input_row.is_charge_by_point or input_row.is_charge_by_download_value
        ):
            # Reason: The returns can't detect correct type limited by if instance block.
            return WaonZaimIncomeRowConverter(input_row)  # type:ignore
        if input_row.is_payment or input_row.is_payment_cancel:
            return cast(ZaimRowConverter[WaonRow, WaonRowData], WaonZaimPaymentRowConverter(input_row))
        if isinstance(input_row, WaonChargeRow) and (
            input_row.is_auto_charge or input_row.is_charge_by_bank_account or input_row.is_charge_by_cash
        ):
            return cast(ZaimRowConverter[WaonRow, WaonRowData], WaonZaimTransferRowConverter(input_row))
        raise ValueError(self.build_message(input_row))

    @staticmethod
    def build_message(input_row: Kind1[WaonRow, WaonRowData]) -> str:
        """This method builds error message."""
        message = f"Unsupported row. Input row = {input_row.__class__.__name__}, {input_row.use_kind}"
        if isinstance(input_row, WaonChargeRow):  # pragma: no cover
            # Reason: This line is insurance for future development so process must be not able to reach
            message = f"{message}, {input_row.charge_kind}"
        return message
