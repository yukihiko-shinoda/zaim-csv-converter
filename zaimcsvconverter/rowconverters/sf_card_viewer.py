"""This module implements convert steps from SFCard Viewer input row to Zaim row."""
from typing import Callable

from zaimcsvconverter.config import SFCardViewerConfig
from zaimcsvconverter.inputcsvformats.sf_card_viewer import SFCardViewerRow, SFCardViewerEnterExitRow
from zaimcsvconverter.zaim_csv_format import ZaimCsvFormat
from zaimcsvconverter.rowconverters import ZaimPaymentRowStoreConverter, ZaimTransferRowConverter, \
    ZaimRowConverterFactory, ZaimRowConverter


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class SFCardViewerZaimPaymentRowConverter(ZaimPaymentRowStoreConverter[SFCardViewerRow]):
    """This class implements convert steps from SFCard Viewer input row to Zaim payment row."""
    account_config: SFCardViewerConfig
    @property
    def cash_flow_source(self) -> str:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        return self.account_config.account_name

    @property
    def note(self) -> str:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        # Reason: Pylint's bug. pylint: disable=no-member
        if not isinstance(self.input_row, SFCardViewerEnterExitRow):
            return ZaimCsvFormat.NOTE_EMPTY
        return (f'{self.input_row.railway_company_name_enter} {self.input_row.station_name_enter}'
                f' → {self.input_row.railway_company_name_exit} {self.input_row.store.name}')

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


class SFCardViewerZaimTransferRowConverter(ZaimTransferRowConverter[SFCardViewerRow]):
    """This class implements convert steps from SFCard Viewer input row to Zaim transfer row."""
    account_config: SFCardViewerConfig
    @property
    def cash_flow_source(self) -> str:
        return self.account_config.auto_charge_source

    @property
    def cash_flow_target(self) -> str:
        return self.account_config.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return -1 * self.input_row.used_amount


class SFCardViewerZaimRowConverterFactory(ZaimRowConverterFactory[SFCardViewerRow]):
    """This class implements select steps from SFCard Viewer input row to Zaim row converter."""
    def __init__(self, account_config: Callable[[], SFCardViewerConfig]):
        self._account_config = account_config

    def create(self, input_row: SFCardViewerRow) -> ZaimRowConverter:
        if input_row.is_transportation or \
                input_row.is_sales_goods or \
                input_row.is_exit_by_window or \
                input_row.is_bus_tram:
            class ConcreteSFCardViewerZaimPaymentRowConverter(SFCardViewerZaimPaymentRowConverter):
                # Reason: Raw code is simple enough. pylint: disable=missing-docstring
                account_config = self._account_config()
            return ConcreteSFCardViewerZaimPaymentRowConverter(input_row)
        if input_row.is_auto_charge:
            class ConcreteSFCardViewerZaimTransferRowConverter(SFCardViewerZaimTransferRowConverter):
                # Reason: Raw code is simple enough. pylint: disable=missing-docstring
                account_config = self._account_config()
            return ConcreteSFCardViewerZaimTransferRowConverter(input_row)
        raise ValueError(f'Unsupported row. class = {type(input_row)}')  # pragma: no cover
        # Reason: This line is insurance for future development so process must be not able to reach
