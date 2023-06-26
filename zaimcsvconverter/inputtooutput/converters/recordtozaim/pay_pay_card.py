"""This module implements convert steps from PayPay Card input row to Zaim row."""


from pathlib import Path

from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.converters.recordtozaim import (
    CsvRecordToZaimRowConverterFactory,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
)
from zaimcsvconverter.inputtooutput.datasources.csv.data.pay_pay_card import PayPayCardRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.pay_pay_card import PayPayCardRow


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
        return PayPayCardZaimPaymentRowConverter(input_row)
