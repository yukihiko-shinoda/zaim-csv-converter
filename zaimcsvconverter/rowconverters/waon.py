"""This module implements convert steps from WAON input row to Zaim row."""
from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.waon import WaonRow, WaonChargeRow
from zaimcsvconverter.rowconverters import ZaimPaymentRowStoreConverter, ZaimTransferRowConverter, \
    ZaimRowConverterFactory, ZaimRowConverter, ZaimIncomeRowStoreConverter


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class WaonZaimIncomeRowConverter(ZaimIncomeRowStoreConverter[WaonRow]):
    """This class implements convert steps from WAON input row to Zaim income row."""
    @property
    def cash_flow_target(self) -> str:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        return CONFIG.waon.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class WaonZaimPaymentRowConverter(ZaimPaymentRowStoreConverter[WaonRow]):
    """This class implements convert steps from WAON input row to Zaim payment row."""
    @property
    def cash_flow_source(self) -> str:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        return CONFIG.waon.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


class WaonZaimTransferRowConverter(ZaimTransferRowConverter[WaonRow]):
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


class WaonZaimRowConverterFactory(ZaimRowConverterFactory[WaonRow]):
    """This class implements select steps from WAON input row to Zaim row converter."""
    def create(self, input_row: WaonRow) -> ZaimRowConverter:
        if isinstance(input_row, WaonChargeRow) and input_row.is_charge_by_point:
            return WaonZaimIncomeRowConverter(input_row)
        if input_row.is_payment:
            return WaonZaimPaymentRowConverter(input_row)
        if isinstance(input_row, WaonChargeRow) and (
                input_row.is_auto_charge or input_row.is_charge_by_bank_account or input_row.is_charge_by_cash
        ):
            return WaonZaimTransferRowConverter(input_row)
        raise ValueError(self.build_message(input_row))

    @staticmethod
    def build_message(input_row: WaonRow) -> str:
        """This method builds error message."""
        message = f'Unsupported row. Input row = {input_row.__class__.__name__}, {input_row.use_kind}'
        if isinstance(input_row, WaonChargeRow):  # pragma: no cover
            # Reason: This line is insurance for future development so process must be not able to reach
            message = f'{message}, {input_row.charge_kind}'
        return message
