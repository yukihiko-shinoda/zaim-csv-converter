"""This module implements convert steps from SFCard Viewer input row to Zaim row."""
from typing import Type, Callable

from zaimcsvconverter.config import SFCardViewerConfig
from zaimcsvconverter.inputcsvformats import ValidatedInputRow
from zaimcsvconverter.inputcsvformats.sf_card_viewer import SFCardViewerRow
from zaimcsvconverter.zaim_row import ZaimRow
from zaimcsvconverter.rowconverters import ZaimPaymentRowConverter, ZaimTransferRowConverter, \
    ZaimRowConverterSelector, ZaimRowConverter


class SFCardViewerZaimPaymentRowConverter(ZaimPaymentRowConverter[SFCardViewerRow]):
    """This class implements convert steps from SFCard Viewer input row to Zaim payment row."""
    account_config: SFCardViewerConfig
    @property
    def _cash_flow_source(self) -> str:
        return self.account_config.account_name

    @property
    def _note(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        input_row = self.validated_input_row.input_row
        if self.validated_input_row.store.name_zaim == '':
            return ZaimRow.NOTE_EMPTY
        return (f'{input_row.railway_company_name_enter} {input_row.station_name_enter}'
                f' → {input_row.railway_company_name_exit} {self.validated_input_row.store.name}')

    @property
    def _amount_payment(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.validated_input_row.input_row.used_amount


class SFCardViewerZaimTransferRowConverter(ZaimTransferRowConverter[SFCardViewerRow]):
    """This class implements convert steps from SFCard Viewer input row to Zaim transfer row."""
    account_config: SFCardViewerConfig
    @property
    def _cash_flow_source(self) -> str:
        return self.account_config.auto_charge_source

    @property
    def _cash_flow_target(self) -> str:
        return self.account_config.account_name

    @property
    def _amount_transfer(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return -1 * self.validated_input_row.input_row.used_amount


class SFCardViewerZaimRowConverterSelector(ZaimRowConverterSelector):
    """This class implements select steps from SFCard Viewer input row to Zaim row converter."""
    def __init__(self, account_config: Callable[[], SFCardViewerConfig]):
        self._account_config = account_config

    def select(self, validated_input_row: ValidatedInputRow[SFCardViewerRow]) -> Type[ZaimRowConverter]:
        input_row = validated_input_row.input_row
        if input_row.is_transportation or \
                input_row.is_sales_goods or \
                input_row.is_exit_by_window or \
                input_row.is_bus_tram:
            class ConcreteSFCardViewerZaimPaymentRowConverter(SFCardViewerZaimPaymentRowConverter):
                # Reason: Raw code is simple enough. pylint: disable=missing-docstring
                account_config = self._account_config()
            return ConcreteSFCardViewerZaimPaymentRowConverter
        if input_row.is_auto_charge:
            class ConcreteSFCardViewerZaimTransferRowConverter(SFCardViewerZaimTransferRowConverter):
                # Reason: Raw code is simple enough. pylint: disable=missing-docstring
                account_config = self._account_config()
            return ConcreteSFCardViewerZaimTransferRowConverter
        raise ValueError(f'Unsupported row. class = {type(input_row)}')
