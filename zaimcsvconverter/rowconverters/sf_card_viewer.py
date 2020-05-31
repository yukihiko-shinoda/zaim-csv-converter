"""This module implements convert steps from SFCard Viewer input row to Zaim row."""
from typing import Callable, Optional

from zaimcsvconverter.config import SFCardViewerConfig
from zaimcsvconverter.inputcsvformats.sf_card_viewer import (
    SFCardViewerEnterExitRow,
    SFCardViewerEnterRow,
    SFCardViewerRow,
)
from zaimcsvconverter.rowconverters import (
    ZaimPaymentRowConverter,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
    ZaimRowConverterFactory,
    ZaimTransferRowConverter,
)
from zaimcsvconverter.zaim_csv_format import ZaimCsvFormat


class SFCardViewerZaimPaymentOnSomewhereRowConverter(ZaimPaymentRowConverter[SFCardViewerRow]):
    """This class implements convert steps from SFCard Viewer row to Zaim payment row."""

    account_config: SFCardViewerConfig

    @property
    def category_large(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return "交通" if self.input_row.is_bus_tram else ZaimCsvFormat.CATEGORY_LARGE_EMPTY

    @property
    def category_small(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return "バス" if self.input_row.is_bus_tram else ZaimCsvFormat.CATEGORY_LARGE_EMPTY

    @property
    def item_name(self) -> str:
        return ZaimCsvFormat.ITEM_NAME_EMPTY

    @property
    def store_name(self) -> str:
        return ZaimCsvFormat.STORE_NAME_EMPTY

    @property
    def cash_flow_source(self) -> str:
        return self.account_config.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class SFCardViewerZaimPaymentOnStationRowConverter(ZaimPaymentRowStoreConverter[SFCardViewerEnterExitRow]):
    """This class implements convert steps from SFCard Viewer enter row to Zaim payment row."""

    account_config: SFCardViewerConfig

    @property
    def cash_flow_source(self) -> str:
        return self.account_config.account_name

    @property
    def note(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        return (
            f"{self.input_row.railway_company_name_enter} {self.input_row.station_name_enter}"
            f" → {self.input_row.railway_company_name_exit} {self.input_row.store.name}"
        )

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


class SFCardViewerZaimTransferRowConverter(ZaimTransferRowConverter[SFCardViewerEnterRow]):
    """This class implements convert steps from SFCard Viewer enter row to Zaim transfer row."""

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
        if isinstance(input_row, SFCardViewerEnterExitRow):

            class ConcreteSFCardViewerZaimPaymentOnStationRowConverter(SFCardViewerZaimPaymentOnStationRowConverter):
                account_config = self._account_config()

            return ConcreteSFCardViewerZaimPaymentOnStationRowConverter(input_row)
        if isinstance(input_row, SFCardViewerEnterRow):

            class ConcreteSFCardViewerZaimTransferRowConverter(SFCardViewerZaimTransferRowConverter):
                account_config = self._account_config()

            return ConcreteSFCardViewerZaimTransferRowConverter(input_row)
        if isinstance(input_row, SFCardViewerRow):

            class ConcreteSFCardViewerZaimPaymentOnSomewhereRowConverter(
                SFCardViewerZaimPaymentOnSomewhereRowConverter
            ):
                account_config = self._account_config()

            return ConcreteSFCardViewerZaimPaymentOnSomewhereRowConverter(input_row)
        raise ValueError(f"Unsupported row. class = {type(input_row)}")  # pragma: no cover
        # Reason: This line is insurance for future development so process must be not able to reach
