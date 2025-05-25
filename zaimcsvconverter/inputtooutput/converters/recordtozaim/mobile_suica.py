"""This module implements convert steps from SFCard Viewer input row to Zaim row."""

from __future__ import annotations

import re
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Callable
from typing import Optional

from zaimcsvconverter.inputtooutput.converters.recordtozaim import CsvRecordToZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimPaymentRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimPaymentRowStoreConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimTransferRowConverter
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.mobile_suica import MobileSuicaRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.mobile_suica import MobileSuicaBusEtCeteraRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.mobile_suica import MobileSuicaEnterExitRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.mobile_suica import MobileSuicaFirstRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.mobile_suica import MobileSuicaRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.mobile_suica import MobileSuicaStoreRow
from zaimcsvconverter.inputtooutput.exporters.zaim.csvfile.zaim_csv_format import ZaimCsvFormat

if TYPE_CHECKING:
    from pathlib import Path

    from returns.primitives.hkt import Kind1

    from zaimcsvconverter.config import SFCardViewerConfig


# Reason: SFCardViewer and Mobile Suica requires same specification
#         and having common ancestor generates extra complexity.
class MobileSuicaZaimPaymentOnSomewhereRowConverter(
    ZaimPaymentRowConverter[MobileSuicaRow, MobileSuicaRowData],
):  # pylint: disable=duplicate-code
    """This class implements convert steps from Mobile Suica row to Zaim payment row."""

    account_config: SFCardViewerConfig
    year: int

    @property
    def date(self) -> datetime:
        return self.input_row.date.replace(year=self.year)

    @property
    def category_large(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return ZaimCsvFormat.CATEGORY_LARGE_EMPTY

    @property
    def category_small(self) -> Optional[str]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return ZaimCsvFormat.CATEGORY_SMALL_EMPTY

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
        return -1 * self.input_row.deposit_used_amount


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class MobileSuicaZaimPaymentOnBusEtCeteraRowConverter(
    ZaimPaymentRowStoreConverter[MobileSuicaBusEtCeteraRow, MobileSuicaRowData],
):
    """This class implements convert steps from Mobile Suica enter row to Zaim payment row."""

    account_config: SFCardViewerConfig
    year: int

    @property
    def date(self) -> datetime:
        return self.input_row.date.replace(year=self.year)

    @property
    def cash_flow_source(self) -> str:
        return self.account_config.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return -1 * self.input_row.deposit_used_amount


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class MobileSuicaZaimPaymentOnStationRowConverter(
    ZaimPaymentRowStoreConverter[MobileSuicaEnterExitRow, MobileSuicaRowData],
):
    """This class implements convert steps from Mobile Suica enter row to Zaim payment row."""

    account_config: SFCardViewerConfig
    year: int

    @property
    def date(self) -> datetime:
        return self.input_row.date.replace(year=self.year)

    @property
    def cash_flow_source(self) -> str:
        return self.account_config.account_name

    @property
    def note(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        return f"{self.input_row.used_place_1} → {self.input_row.store.name}"

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return -1 * self.input_row.deposit_used_amount


class MobileSuicaZaimTransferRowConverter(ZaimTransferRowConverter[MobileSuicaStoreRow, MobileSuicaRowData]):
    """This class implements convert steps from Mobile Suica enter row to Zaim transfer row."""

    account_config: SFCardViewerConfig
    year: int

    @property
    def date(self) -> datetime:
        return self.input_row.date.replace(year=self.year)

    @property
    def cash_flow_source(self) -> str:
        return self.account_config.auto_charge_source

    @property
    def cash_flow_target(self) -> str:
        return self.account_config.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.deposit_used_amount


class MobileSuicaZaimTransferFirstRowConverter(ZaimTransferRowConverter[MobileSuicaFirstRow, MobileSuicaRowData]):
    """This class implements convert steps from Mobile Suica enter row to Zaim transfer row."""

    account_config: SFCardViewerConfig
    year: int

    @property
    def date(self) -> datetime:
        return self.input_row.date.replace(year=self.year)

    @property
    def cash_flow_source(self) -> str:
        return self.account_config.auto_charge_source

    @property
    def cash_flow_target(self) -> str:
        return self.account_config.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.balance


class MobileSuicaZaimRowConverterFactory(CsvRecordToZaimRowConverterFactory[MobileSuicaRow, MobileSuicaRowData]):
    """This class implements select steps from Mobile Suica input row to Zaim row converter."""

    def __init__(self, account_config: Callable[[], SFCardViewerConfig]) -> None:
        self._account_config = account_config
        self.year: int = 0

    def create(
        self,
        # Reason: Maybe, there are no way to resolve.
        # The nearest issues: https://github.com/dry-python/returns/issues/708
        input_row: Kind1[MobileSuicaRow, MobileSuicaRowData],  # type: ignore[override]
        path_csv_file: Path,
    ) -> ZaimRowConverter[MobileSuicaRow, MobileSuicaRowData]:
        self.year = (
            # Reason: Time is not used in this process.
            datetime.strptime(re.findall(r"_(\d{4,6})", path_csv_file.stem)[-1][0:4], "%Y").year  # noqa: DTZ007
        )
        if isinstance(input_row, MobileSuicaFirstRow):

            class ConcreteMobileSuicaZaimTransferFirstRowConverter(MobileSuicaZaimTransferFirstRowConverter):
                account_config = self._account_config()
                year = self.year

            # Reason: The returns can't detect correct type limited by if instance block.
            return ConcreteMobileSuicaZaimTransferFirstRowConverter(input_row)  # type: ignore[return-value,arg-type]
        if isinstance(input_row, MobileSuicaBusEtCeteraRow):

            class ConcreteMobileSuicaZaimPaymentOnBusEtCeteraRowConverter(
                MobileSuicaZaimPaymentOnBusEtCeteraRowConverter,
            ):
                account_config = self._account_config()
                year = self.year

            # Reason: The returns can't detect correct type limited by if instance block.
            return ConcreteMobileSuicaZaimPaymentOnBusEtCeteraRowConverter(  # type: ignore[return-value]
                input_row,  # type: ignore[arg-type]
            )
        if isinstance(input_row, MobileSuicaEnterExitRow):

            class ConcreteMobileSuicaZaimPaymentOnStationRowConverter(MobileSuicaZaimPaymentOnStationRowConverter):
                account_config = self._account_config()
                year = self.year

            # Reason: The returns can't detect correct type limited by if instance block.
            return ConcreteMobileSuicaZaimPaymentOnStationRowConverter(
                input_row,  # type: ignore[return-value,arg-type]
            )
        return self._create(input_row)

    def _create(
        self,
        input_row: Kind1[MobileSuicaRow, MobileSuicaRowData],
    ) -> ZaimRowConverter[MobileSuicaRow, MobileSuicaRowData]:
        if isinstance(input_row, MobileSuicaStoreRow):

            class ConcreteMobileSuicaZaimTransferRowConverter(MobileSuicaZaimTransferRowConverter):
                account_config = self._account_config()
                year = self.year

            # Reason: The returns can't detect correct type limited by if instance block.
            return ConcreteMobileSuicaZaimTransferRowConverter(input_row)  # type: ignore[return-value,arg-type]
        if isinstance(input_row, MobileSuicaRow):

            class ConcreteMobileSuicaZaimPaymentOnSomewhereRowConverter(MobileSuicaZaimPaymentOnSomewhereRowConverter):
                account_config = self._account_config()
                year = self.year

            return ConcreteMobileSuicaZaimPaymentOnSomewhereRowConverter(input_row)
        msg = f"Unsupported row. class = {type(input_row)}"
        raise ValueError(msg)  # pragma: no cover
        # Reason: This line is insurance for future development so process must be not able to reach
