"""This module implements convert steps from PayPay Card input row to Zaim row."""

from pathlib import Path
from typing import cast, Optional

from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.converters.recordtozaim import (
    CsvRecordToZaimRowConverterFactory,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
    ZaimTransferRowConverter,
)
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.pay_pay_card import PayPayCardRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.pay_pay_card import PayPayCardRow


class PayPayCardZaimTransferRowConverter(ZaimTransferRowConverter[PayPayCardRow, PayPayCardRowData]):
    """This class implements convert steps from GOLD POINT CARD + input row to Zaim transfer row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.pay_pay_card.account_name

    @property
    def cash_flow_target(self) -> Optional[str]:
        return self.input_row.store.transfer_target

    @property
    def amount(self) -> int:
        return self.input_row.used_amount


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class PayPayCardZaimPaymentRowConverter(ZaimPaymentRowStoreConverter[PayPayCardRow, PayPayCardRowData]):
    """This class implements convert steps from PayPay Card input row to Zaim payment row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.pay_pay_card.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.used_amount


class PayPayCardZaimRowConverterFactory(CsvRecordToZaimRowConverterFactory[PayPayCardRow, PayPayCardRowData]):
    """This class implements select steps from PayPay Card input row to Zaim row converter."""

    def create(
        self,
        # Reason: Maybe, there are no way to resolve.
        # The nearest issues: https://github.com/dry-python/returns/issues/708
        input_row: Kind1[PayPayCardRow, PayPayCardRowData],  # type: ignore[override]
        _path_csv_file: Path,
    ) -> ZaimRowConverter[PayPayCardRow, PayPayCardRowData]:
        dekinded_input_row = cast("PayPayCardRow", input_row)
        if dekinded_input_row.store.transfer_target:
            return PayPayCardZaimTransferRowConverter(input_row)
        return PayPayCardZaimPaymentRowConverter(input_row)
