"""This module implements row model of SBI Sumishin net bank CSV."""

from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.sbi_sumishin_net_bank import SBISumishinNetBankRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import InputStoreRow


class SBISumishinNetBankRow(InputStoreRow[SBISumishinNetBankRowData]):
    """This class implements row model of SBI Sumishin net bank CSV."""

    CONTENT_ORDINARY_PRIMARY_ACCOUNT = "普通　代表口座"
    # Reason: Specification.
    CONTENT_SBI_HYBRID_DEPOSIT = "ＳＢＩハイブリッド預金"
    CONTENT_INTEREST = "利息"
    CONTENT_NATIONAL_TAX = "国税"
    CONTENT_REGIONAL_TAX = "地方税"
    # Reason: Specification.
    CONTENT_TRANSFER_SBI_SECURITIES = "振替　ＳＢＩ証券"
    # Reason: Specification.
    CONTENT_PREFIX_ATM = "ＡＴＭ"  # noqa: RUF001

    @property
    def is_row_to_skip(self) -> bool:
        # Zaim seems to manage both primary account and SBI hybrid deposit in one SBI Sumishin net bank account.
        return self.is_ordinary_primary_account or self.is_sbi_hybrid_deposit

    @property
    def is_transaction_with_others(self) -> bool:
        return self.is_interest or self.is_national_tax or self.is_regional_tax

    @property
    def is_transfer(self) -> bool:
        return self.is_transfer_sbi_securities or self.is_atm

    @property
    def is_ordinary_primary_account(self) -> bool:
        return self.store.name == self.CONTENT_ORDINARY_PRIMARY_ACCOUNT

    @property
    def is_sbi_hybrid_deposit(self) -> bool:
        return self.store.name == self.CONTENT_SBI_HYBRID_DEPOSIT

    @property
    def is_interest(self) -> bool:
        return self.store.name == self.CONTENT_INTEREST

    @property
    def is_national_tax(self) -> bool:
        return self.store.name == self.CONTENT_NATIONAL_TAX

    @property
    def is_regional_tax(self) -> bool:
        return self.store.name == self.CONTENT_REGIONAL_TAX

    @property
    def is_transfer_sbi_securities(self) -> bool:
        return self.store.name == self.CONTENT_TRANSFER_SBI_SECURITIES

    @property
    def is_atm(self) -> bool:
        return self.store.name is not None and self.store.name.startswith(self.CONTENT_PREFIX_ATM)


class SBISumishinNetBankWithdrawalRow(SBISumishinNetBankRow):
    """This class implements row model of SBI Sumishin net bank CSV."""

    def __init__(self, input_row_data: SBISumishinNetBankRowData, *args: object, **kwargs: object) -> None:
        super().__init__(input_row_data, FileCsvConvert.SBI_SUMISHIN_NET_BANK.value, *args, **kwargs)
        if input_row_data.withdrawal_amount is None:
            raise TypeError
        self.withdrawal_amount = input_row_data.withdrawal_amount


class SBISumishinNetBankDepositRow(SBISumishinNetBankRow):
    """This class implements row model of SBI Sumishin net bank CSV."""

    def __init__(self, input_row_data: SBISumishinNetBankRowData, *args: object, **kwargs: object) -> None:
        super().__init__(input_row_data, FileCsvConvert.SBI_SUMISHIN_NET_BANK.value, *args, **kwargs)
        if input_row_data.deposit_amount is None:
            raise TypeError
        self.deposit_amount = input_row_data.deposit_amount
