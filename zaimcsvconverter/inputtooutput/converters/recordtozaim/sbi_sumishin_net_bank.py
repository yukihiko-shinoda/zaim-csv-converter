"""This module implements convert steps from SBI Sumishin net bank input row to Zaim row."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Union
from typing import cast

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.converters.recordtozaim import CsvRecordToZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimIncomeRowStoreConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimPaymentRowStoreConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimTransferRowConverter
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.sbi_sumishin_net_bank import SBISumishinNetBankRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.sbi_sumishin_net_bank import (
    SBISumishinNetBankDepositRow,  # noqa: H301,RUF100
)
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.sbi_sumishin_net_bank import SBISumishinNetBankRow
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.sbi_sumishin_net_bank import (
    SBISumishinNetBankWithdrawalRow,  # noqa: H301,RUF100
)

if TYPE_CHECKING:
    from pathlib import Path

    from returns.primitives.hkt import Kind1


class SBISumishinNetBankZaimPaymentRowConverter(
    ZaimPaymentRowStoreConverter[SBISumishinNetBankWithdrawalRow, SBISumishinNetBankRowData],
):
    """This class implements convert steps from MUFG input row to Zaim income row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.sbi_sumishin_net_bank.account_name

    @property
    def amount(self) -> int:
        return self.input_row.withdrawal_amount


class SBISumishinNetBankWithdrawalZaimTransferRowConverter(
    ZaimTransferRowConverter[SBISumishinNetBankWithdrawalRow, SBISumishinNetBankRowData],
):
    """This class implements convert steps from MUFG income input row to Zaim transfer row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.sbi_sumishin_net_bank.account_name

    @property
    def cash_flow_target(self) -> str | None:
        return self.input_row.store.transfer_target

    @property
    def amount(self) -> int:
        return self.input_row.withdrawal_amount


class SBISumishinNetBankZaimIncomeRowConverter(
    ZaimIncomeRowStoreConverter[SBISumishinNetBankDepositRow, SBISumishinNetBankRowData],
):
    """This class implements convert steps from MUFG input row to Zaim income row."""

    @property
    def cash_flow_target(self) -> str:
        return CONFIG.sbi_sumishin_net_bank.account_name

    @property
    def amount(self) -> int:
        return self.input_row.deposit_amount


class SBISumishinNetBankDepositZaimTransferRowConverter(
    ZaimTransferRowConverter[SBISumishinNetBankDepositRow, SBISumishinNetBankRowData],
):
    """This class implements convert steps from MUFG income input row to Zaim transfer row."""

    @property
    def cash_flow_source(self) -> str | None:
        return self.input_row.store.transfer_target

    @property
    def cash_flow_target(self) -> str:
        return CONFIG.sbi_sumishin_net_bank.account_name

    @property
    def amount(self) -> int:
        return self.input_row.deposit_amount


AnySbiSumishinNetBankConverter = Union[
    SBISumishinNetBankZaimPaymentRowConverter,
    SBISumishinNetBankWithdrawalZaimTransferRowConverter,
    SBISumishinNetBankZaimIncomeRowConverter,
    SBISumishinNetBankDepositZaimTransferRowConverter,
]


class SBISumishinNetBankZaimRowConverterFactory(
    CsvRecordToZaimRowConverterFactory[SBISumishinNetBankRow, SBISumishinNetBankRowData],
):
    """This class implements select steps from MUFG input row to Zaim row converter."""

    KEY_INSTANCE_TYPE_INSTANCE_OF_WITHDRAWAL_ROW = "instance_of_withdrawal_row"
    KEY_INSTANCE_TYPE_INSTANCE_OF_DEPOSIT_ROW = "instance_of_deposit_row"
    KEY_TRANSACTION_TYPE_TRANSACTION_WITH_OTHERS = "transaction_with_others"
    KEY_TRANSACTION_TYPE_TRANSFER = "transfer"

    def create(
        self,
        # Reason: Maybe, there are no way to resolve.
        # The nearest issues: https://github.com/dry-python/returns/issues/708
        input_row: Kind1[SBISumishinNetBankRow, SBISumishinNetBankRowData],  # type: ignore[override]
        _: Path,
    ) -> ZaimRowConverter[SBISumishinNetBankRow, SBISumishinNetBankRowData]:
        dictionary: dict[str, dict[str, type[AnySbiSumishinNetBankConverter]]] = {
            self.KEY_INSTANCE_TYPE_INSTANCE_OF_WITHDRAWAL_ROW: {
                self.KEY_TRANSACTION_TYPE_TRANSACTION_WITH_OTHERS: SBISumishinNetBankZaimPaymentRowConverter,
                self.KEY_TRANSACTION_TYPE_TRANSFER: SBISumishinNetBankWithdrawalZaimTransferRowConverter,
            },
            self.KEY_INSTANCE_TYPE_INSTANCE_OF_DEPOSIT_ROW: {
                self.KEY_TRANSACTION_TYPE_TRANSACTION_WITH_OTHERS: SBISumishinNetBankZaimIncomeRowConverter,
                self.KEY_TRANSACTION_TYPE_TRANSFER: SBISumishinNetBankDepositZaimTransferRowConverter,
            },
        }
        instance_type = self.check_instance_type(input_row)
        transaction_type = self.check_transaction_type(input_row)
        # Reason: The returns can't detect correct type limited by if instance block.
        converter = dictionary[instance_type][transaction_type](input_row)  # type: ignore[arg-type]
        return cast("ZaimRowConverter[SBISumishinNetBankRow, SBISumishinNetBankRowData]", converter)

    def check_transaction_type(self, input_row: Kind1[SBISumishinNetBankRow, SBISumishinNetBankRowData]) -> str:
        dekinded_input_row = cast("SBISumishinNetBankRow", input_row)
        if dekinded_input_row.is_transaction_with_others:
            return self.KEY_TRANSACTION_TYPE_TRANSACTION_WITH_OTHERS
        if dekinded_input_row.is_transfer:
            return self.KEY_TRANSACTION_TYPE_TRANSFER
        raise ValueError(self.build_message(input_row))  # pragma: no cover

    def check_instance_type(self, input_row: Kind1[SBISumishinNetBankRow, SBISumishinNetBankRowData]) -> str:
        if isinstance(input_row, SBISumishinNetBankWithdrawalRow):
            return self.KEY_INSTANCE_TYPE_INSTANCE_OF_WITHDRAWAL_ROW
        if isinstance(input_row, SBISumishinNetBankDepositRow):
            return self.KEY_INSTANCE_TYPE_INSTANCE_OF_DEPOSIT_ROW
        raise ValueError(self.build_message(input_row))  # pragma: no cover

    @staticmethod
    def build_message(input_row: Kind1[SBISumishinNetBankRow, SBISumishinNetBankRowData]) -> str:  # pragma: no cover
        """This method builds error message."""
        dekinded_input_row = cast("SBISumishinNetBankRow", input_row)
        return (
            "Unsupported row. "
            f"class = {type(input_row)}, "
            f"{dekinded_input_row.date=}, "
            f"{dekinded_input_row.store.name=}, "
            f"{dekinded_input_row.is_transaction_with_others=}, "
            f"{dekinded_input_row.is_transfer=}"
        )
