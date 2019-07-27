"""This module implements convert steps from WAON input row to Zaim row."""
from typing import Type

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.waon import WaonRow, WaonChargeRow
from zaimcsvconverter.rowconverters import ZaimIncomeRowConverter, ZaimPaymentRowConverter, ZaimTransferRowConverter, \
    ZaimRowConverterSelector, ZaimRowConverter


class WaonZaimIncomeRowConverter(ZaimIncomeRowConverter[WaonRow]):
    """This class implements convert steps from WAON input row to Zaim income row."""
    @property
    def _cash_flow_target(self) -> str:
        return CONFIG.waon.account_name

    @property
    def _amount_income(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


class WaonZaimPaymentRowConverter(ZaimPaymentRowConverter[WaonRow]):
    """This class implements convert steps from WAON input row to Zaim payment row."""
    @property
    def _cash_flow_source(self) -> str:
        return CONFIG.waon.account_name

    @property
    def _amount_payment(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


class WaonZaimTransferRowConverter(ZaimTransferRowConverter[WaonRow]):
    """This class implements convert steps from WAON input row to Zaim transfer row."""
    @property
    def _cash_flow_source(self) -> str:
        return CONFIG.waon.auto_charge_source

    @property
    def _cash_flow_target(self) -> str:
        return CONFIG.waon.account_name

    @property
    def _amount_transfer(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


class WaonZaimRowConverterSelector(ZaimRowConverterSelector[WaonRow]):
    """This class implements select steps from WAON input row to Zaim row converter."""
    def select(self, input_row: WaonRow) -> Type[ZaimRowConverter]:
        if isinstance(input_row, WaonChargeRow) and input_row.is_charge_by_point:
            return WaonZaimIncomeRowConverter
        if input_row.is_payment:
            return WaonZaimPaymentRowConverter
        if isinstance(input_row, WaonChargeRow) and (input_row.is_auto_charge or input_row.is_charge_by_bank_account):
            return WaonZaimTransferRowConverter
        raise ValueError(f'Unsupported row. Input row = {type(input_row)}, {input_row.use_kind}, '
                         f'{input_row.charge_kind if isinstance(input_row, WaonChargeRow) else ""}')
