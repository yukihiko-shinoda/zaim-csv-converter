"""This module implements convert steps from PayPay Card input row to Zaim row (2025-05 format)."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import cast

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.converters.recordtozaim import CsvRecordToZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimPaymentRowStoreConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimTransferRowConverter
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.pay_pay_card_202505 import PayPayCard202505RowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.pay_pay_card_202505 import PayPayCard202505Row

if TYPE_CHECKING:
    from pathlib import Path

    from returns.primitives.hkt import Kind1


class PayPayCard202505ZaimTransferRowConverter(
    ZaimTransferRowConverter[PayPayCard202505Row, PayPayCard202505RowData],
):
    """This class implements convert steps from GOLD POINT CARD + input row to Zaim transfer row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.pay_pay_card.account_name

    @property
    def cash_flow_target(self) -> str | None:
        return self.input_row.store.transfer_target

    @property
    def amount(self) -> int:
        return self.input_row.used_amount


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class PayPayCard202505ZaimPaymentRowConverter(
    ZaimPaymentRowStoreConverter[PayPayCard202505Row, PayPayCard202505RowData],
):
    """This class implements convert steps from PayPay Card input row to Zaim payment row (2025-05 format)."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.pay_pay_card.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


class PayPayCard202505ZaimRowConverterFactory(
    CsvRecordToZaimRowConverterFactory[PayPayCard202505Row, PayPayCard202505RowData],
):
    """This class implements select steps from PayPay Card input row to Zaim row converter (2025-05 format)."""

    def create(
        self,
        # Reason: Maybe, there are no way to resolve.
        # The nearest issues: https://github.com/dry-python/returns/issues/708
        input_row: Kind1[PayPayCard202505Row, PayPayCard202505RowData],  # type: ignore[override]
        _path_csv_file: Path,
    ) -> ZaimRowConverter[PayPayCard202505Row, PayPayCard202505RowData]:
        dekinded_input_row = cast("PayPayCard202505Row", input_row)
        if dekinded_input_row.store.transfer_target:
            return PayPayCard202505ZaimTransferRowConverter(input_row)
        return PayPayCard202505ZaimPaymentRowConverter(input_row)
