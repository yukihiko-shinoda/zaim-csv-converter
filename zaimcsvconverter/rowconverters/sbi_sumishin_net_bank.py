"""This module implements convert steps from SBI Sumishin net bank input row to Zaim row."""
from typing import cast

from returns.primitives.hkt import Kind1

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.sbi_sumishin_net_bank import (
    SBISumishinNetBankDepositRow,
    SBISumishinNetBankRow,
    SBISumishinNetBankRowData,
    SBISumishinNetBankWithdrawalRow,
)
from zaimcsvconverter.rowconverters import (
    ZaimIncomeRowStoreConverter,
    ZaimPaymentRowStoreConverter,
    ZaimRowConverter,
    ZaimRowConverterFactory,
    ZaimTransferRowConverter,
)


class SBISumishinNetBankZaimPaymentRowConverter(
    ZaimPaymentRowStoreConverter[SBISumishinNetBankWithdrawalRow, SBISumishinNetBankRowData]
):
    """This class implements convert steps from MUFG input row to Zaim income row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.sbi_sumishin_net_bank.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.withdrawal_amount


class SBISumishinNetBankWithdrawalZaimTransferRowConverter(
    ZaimTransferRowConverter[SBISumishinNetBankWithdrawalRow, SBISumishinNetBankRowData]
):
    """This class implements convert steps from MUFG income input row to Zaim transfer row."""

    @property
    def cash_flow_source(self) -> str:
        return CONFIG.sbi_sumishin_net_bank.account_name

    @property
    def cash_flow_target(self) -> str:
        return self.input_row.store.transfer_target

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.withdrawal_amount


class SBISumishinNetBankZaimIncomeRowConverter(
    ZaimIncomeRowStoreConverter[SBISumishinNetBankDepositRow, SBISumishinNetBankRowData]
):
    """This class implements convert steps from MUFG input row to Zaim income row."""

    @property
    def cash_flow_target(self) -> str:
        return CONFIG.sbi_sumishin_net_bank.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.deposit_amount


class SBISumishinNetBankDepositZaimTransferRowConverter(
    ZaimTransferRowConverter[SBISumishinNetBankDepositRow, SBISumishinNetBankRowData]
):
    """This class implements convert steps from MUFG income input row to Zaim transfer row."""

    @property
    def cash_flow_source(self) -> str:
        return self.input_row.store.transfer_target

    @property
    def cash_flow_target(self) -> str:
        return CONFIG.sbi_sumishin_net_bank.account_name

    @property
    def amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.deposit_amount


class SBISumishinNetBankZaimRowConverterFactory(
    ZaimRowConverterFactory[SBISumishinNetBankRow, SBISumishinNetBankRowData]
):
    """This class implements select steps from MUFG input row to Zaim row converter."""

    def create(
        self, input_row: Kind1[SBISumishinNetBankRow, SBISumishinNetBankRowData]
    ) -> ZaimRowConverter[SBISumishinNetBankRow, SBISumishinNetBankRowData]:
        dekinded_input_row = cast(SBISumishinNetBankRow, input_row)
        converter = None
        if isinstance(input_row, SBISumishinNetBankWithdrawalRow) and dekinded_input_row.is_transaction_with_others:
            # Reason: The returns can't detect correct type limited by if instance block.
            converter = SBISumishinNetBankZaimPaymentRowConverter(input_row)  # type: ignore
        elif isinstance(input_row, SBISumishinNetBankWithdrawalRow) and dekinded_input_row.is_transfer:
            # Reason: The returns can't detect correct type limited by if instance block.
            converter = SBISumishinNetBankWithdrawalZaimTransferRowConverter(input_row)  # type: ignore
        elif isinstance(input_row, SBISumishinNetBankDepositRow) and dekinded_input_row.is_transaction_with_others:
            # Reason: The returns can't detect correct type limited by if instance block.
            converter = SBISumishinNetBankZaimIncomeRowConverter(input_row)  # type: ignore
        elif isinstance(input_row, SBISumishinNetBankDepositRow) and dekinded_input_row.is_transfer:
            # Reason: The returns can't detect correct type limited by if instance block.
            converter = SBISumishinNetBankDepositZaimTransferRowConverter(input_row)  # type: ignore
        else:
            raise ValueError(self.build_message(input_row))  # pragma: no cover
        return cast(ZaimRowConverter[SBISumishinNetBankRow, SBISumishinNetBankRowData], converter)
        # Reason: This line is insurance for future development so process must be not able to reach

    @staticmethod
    def build_message(input_row: Kind1[SBISumishinNetBankRow, SBISumishinNetBankRowData]) -> str:  # pragma: no cover
        """This method builds error message."""
        dekinded_input_row = cast(SBISumishinNetBankRow, input_row)
        return (
            "Unsupported row. "
            f"class = {type(input_row)}, "
            f"{dekinded_input_row.date=}, "
            f"{dekinded_input_row.store.name=}, "
            f"{dekinded_input_row.is_transaction_with_others=}, "
            f"{dekinded_input_row.is_transfer=}"
        )
