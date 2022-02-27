"""This module implements row model of SBI Sumishin net bank CSV."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from pydantic.dataclasses import dataclass as pydantic_dataclass

from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputcsvformats import AbstractPydantic, InputRowFactory, InputStoreRow, InputStoreRowData
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_datetime import StringToDateTime
from zaimcsvconverter.inputcsvformats.customdatatypes.string_to_optional_int import (
    ConstrainedStringWithCommaToOptionalInt,
)


@pydantic_dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class SBISumishinNetBankRowDataPydantic(AbstractPydantic):
    """This class implements data class for wrapping list of SF Card Viewer CSV row model."""

    date: StringToDateTime
    content: str
    withdrawal_amount: ConstrainedStringWithCommaToOptionalInt
    deposit_amount: ConstrainedStringWithCommaToOptionalInt
    balance: str
    note: str


@dataclass
class SBISumishinNetBankRowData(InputStoreRowData[SBISumishinNetBankRowDataPydantic]):
    """This class implements data class for wrapping list of SBI Sumishin net bank CSV row model."""

    _date: str
    _content: str
    _withdrawal_amount: str
    _deposit_amount: str
    balance: str
    note: str

    def create_pydantic(self) -> SBISumishinNetBankRowDataPydantic:
        return SBISumishinNetBankRowDataPydantic(
            # Reason: Maybe, there are no way to specify type before converted by pydantic
            self._date,  # type: ignore
            self._content,
            self._withdrawal_amount,  # type: ignore
            self._deposit_amount,  # type: ignore
            self.balance,
            self.note,
        )

    @property
    def date(self) -> datetime:
        return self.pydantic.date

    @property
    def store_name(self) -> str:
        return self.pydantic.content

    @property
    def withdrawal_amount(self) -> Optional[int]:
        return self.pydantic.withdrawal_amount

    @property
    def deposit_amount(self) -> Optional[int]:
        return self.pydantic.deposit_amount


class SBISumishinNetBankRow(InputStoreRow[SBISumishinNetBankRowData]):
    """This class implements row model of SBI Sumishin net bank CSV."""

    CONTENT_ORDINARY_PRIMARY_ACCOUNT = "普通　代表口座"
    CONTENT_SBI_HYBRID_DEPOSIT = "ＳＢＩハイブリッド預金"
    CONTENT_INTEREST = "利息"
    CONTENT_TRANSFER_SBI_SECURITIES = "振替　ＳＢＩ証券"
    CONTENT_PREFIX_ATM = "ＡＴＭ"

    @property
    def is_row_to_skip(self) -> bool:
        # Zaim seems to manage both primary account and SBI hybrid deposit in one SBI Sumishin net bank account.
        return self.is_ordinary_primary_account or self.is_sbi_hybrid_deposit

    @property
    def is_transaction_with_others(self) -> bool:
        return self.is_interest

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
    def is_transfer_sbi_securities(self) -> bool:
        return self.store.name == self.CONTENT_TRANSFER_SBI_SECURITIES

    @property
    def is_atm(self) -> bool:
        return self.store.name.startswith(self.CONTENT_PREFIX_ATM)


class SBISumishinNetBankWithdrawalRow(SBISumishinNetBankRow):
    """This class implements row model of SBI Sumishin net bank CSV."""

    def __init__(self, input_row_data: SBISumishinNetBankRowData, *args: Any, **kwargs: Any):
        super().__init__(input_row_data, FileCsvConvert.SBI_SUMISHIN_NET_BANK.value, *args, **kwargs)
        if input_row_data.withdrawal_amount is None:
            raise TypeError
        self.withdrawal_amount = input_row_data.withdrawal_amount


class SBISumishinNetBankDepositRow(SBISumishinNetBankRow):
    """This class implements row model of SBI Sumishin net bank CSV."""

    def __init__(self, input_row_data: SBISumishinNetBankRowData, *args: Any, **kwargs: Any):
        super().__init__(input_row_data, FileCsvConvert.SBI_SUMISHIN_NET_BANK.value, *args, **kwargs)
        if input_row_data.deposit_amount is None:
            raise TypeError
        self.deposit_amount = input_row_data.deposit_amount


class SBISumishinNetBankRowFactory(InputRowFactory[SBISumishinNetBankRowData, SBISumishinNetBankRow]):
    """This class implements factory to create MUFG CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: SBISumishinNetBankRowData) -> SBISumishinNetBankRow:  # type: ignore
        if input_row_data.deposit_amount is None and input_row_data.withdrawal_amount is not None:
            return SBISumishinNetBankWithdrawalRow(input_row_data)
        if input_row_data.deposit_amount is not None and input_row_data.withdrawal_amount is None:
            return SBISumishinNetBankDepositRow(input_row_data)
        raise ValueError(
            "Deposit amount and withdrawal amount is not supported. "
            f"{input_row_data.date=}, {input_row_data.deposit_amount=}, {input_row_data.withdrawal_amount=}"
        )  # pragma: no cover
