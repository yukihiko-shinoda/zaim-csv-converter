"""This module implements convert steps from SBI Sumishin net bank input row to Zaim row."""
from typing import cast, Union

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

    KEY_INSTANCE_TYPE_INSTANCE_OF_WITHDRAWAL_ROW = "instance_of_withdrawal_row"
    KEY_INSTANCE_TYPE_INSTANCE_OF_DEPOSIT_ROW = "instance_of_deposit_row"
    KEY_TRANSACTION_TYPE_TRANSACTION_WITH_OTHERS = "transaction_with_others"
    KEY_TRANSACTION_TYPE_TRANSFER = "transfer"

    def create(
        self, input_row: Kind1[SBISumishinNetBankRow, SBISumishinNetBankRowData]
    ) -> ZaimRowConverter[SBISumishinNetBankRow, SBISumishinNetBankRowData]:
        dictionary: dict[
            str,
            dict[
                str,
                type[
                    Union[
                        SBISumishinNetBankZaimPaymentRowConverter,
                        SBISumishinNetBankWithdrawalZaimTransferRowConverter,
                        SBISumishinNetBankZaimIncomeRowConverter,
                        SBISumishinNetBankDepositZaimTransferRowConverter,
                    ]
                ],
            ],
        ] = {
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
        converter = dictionary[instance_type][transaction_type](input_row)  # type: ignore
        return cast(ZaimRowConverter[SBISumishinNetBankRow, SBISumishinNetBankRowData], converter)

    def check_transaction_type(self, input_row: Kind1[SBISumishinNetBankRow, SBISumishinNetBankRowData]) -> str:
        dekinded_input_row = cast(SBISumishinNetBankRow, input_row)
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
        dekinded_input_row = cast(SBISumishinNetBankRow, input_row)
        return (
            "Unsupported row. "
            f"class = {type(input_row)}, "
            f"{dekinded_input_row.date=}, "
            f"{dekinded_input_row.store.name=}, "
            f"{dekinded_input_row.is_transaction_with_others=}, "
            f"{dekinded_input_row.is_transfer=}"
        )
