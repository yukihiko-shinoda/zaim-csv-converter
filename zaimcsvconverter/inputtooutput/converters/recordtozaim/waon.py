"""This module implements convert steps from WAON input row to Zaim row."""

from pathlib import Path
from typing import cast

from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.converters.recordtozaim import (
    CsvRecordToZaimRowConverterFactory,
    ZaimIncomeRowStoreConverter,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
    ZaimTransferRowConverter,
)
from zaimcsvconverter.inputtooutput.datasources.csv.data.waon import WaonRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.waon import WaonChargeRow, WaonRow, WaonStoreRow


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
class WaonZaimPaymentRowConverter(ZaimPaymentRowStoreConverter[WaonStoreRow, WaonRowData]):
    """This class implements convert steps from WAON input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.waon.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return -self.input_row.used_amount if self.input_row.is_payment_cancel else self.input_row.used_amount


class WaonZaimTransferRowConverter(ZaimTransferRowConverter[WaonStoreRow, WaonRowData]):
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

    def create(
        self,
        # Reason: Maybe, there are no way to resolve.
        # The nearest issues: https://github.com/dry-python/returns/issues/708
        input_row: Kind1[WaonRow, WaonRowData],  # type: ignore[override]
        _path_csv_file: Path,
    ) -> ZaimRowConverter[WaonRow, WaonRowData]:
        if isinstance(input_row, WaonChargeRow):
            return self.create_charge(input_row)
        if isinstance(input_row, WaonStoreRow):
            return self.create_store(input_row)
        dekinded_input_row = cast(WaonRow, input_row)
        raise ValueError(self.build_message(dekinded_input_row))

    def create_charge(self, input_row: WaonChargeRow) -> ZaimRowConverter[WaonRow, WaonRowData]:
        """This method creates Zaim row converter for charge row."""
        if input_row.is_income:
            # Reason: The returns can't detect correct type limited by if instance block.
            return WaonZaimIncomeRowConverter(input_row)  # type: ignore[arg-type,return-value]
        if input_row.is_transfer:
            # Reason: The returns can't detect correct type limited by if instance block.
            return WaonZaimTransferRowConverter(input_row)  # type: ignore[arg-type,return-value]
        raise ValueError(self.build_message(input_row))

    def create_store(self, input_row: WaonStoreRow) -> ZaimRowConverter[WaonRow, WaonRowData]:
        if input_row.is_payment or input_row.is_payment_cancel:
            # Reason: The returns can't detect correct type limited by if instance block.
            return WaonZaimPaymentRowConverter(input_row)  # type: ignore[arg-type,return-value]
        raise ValueError(self.build_message(input_row))

    @staticmethod
    def build_message(input_row: WaonRow) -> str:
        """This method builds error message."""
        message = f"Unsupported row. Input row = {input_row.__class__.__name__}, {input_row.use_kind}"
        if isinstance(input_row, WaonChargeRow):  # pragma: no cover
            # Reason: This line is insurance for future development so process must be not able to reach
            message = f"{message}, {input_row.charge_kind}"
        return message
