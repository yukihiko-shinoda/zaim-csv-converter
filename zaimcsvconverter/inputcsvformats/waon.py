"""This module implements row model of WAON CSV."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
import re
from typing import Optional
from dataclasses import dataclass

from zaimcsvconverter.exceptions import InvalidRowError
from zaimcsvconverter.inputcsvformats import InputStoreRowData, InputStoreRow, InputRowFactory, ValidatedInputStoreRow
from zaimcsvconverter.models import Store, AccountId


@dataclass
class WaonRowData(InputStoreRowData):
    """This class implements data class for wrapping list of WAON CSV row model."""
    _date: str
    _used_store: str
    used_amount: str
    use_kind: str
    charge_kind: str

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        return self._used_store


class WaonRow(InputStoreRow):
    """This class implements row model of WAON CSV."""
    class UseKind(Enum):
        """This class implements constant of user kind in WAON CSV."""
        PAYMENT = '支払'
        CHARGE = 'チャージ'
        AUTO_CHARGE = 'オートチャージ'
        DOWNLOAD_POINT = 'ポイントダウンロード'

    class ChargeKind(Enum):
        """This class implements constant of charge kind in WAON CSV."""
        BANK_ACCOUNT = '銀行口座'
        POINT = 'ポイント'

    def __init__(self, account_id: AccountId, row_data: WaonRowData):
        super().__init__(account_id, row_data)
        matches = re.search(r'([\d,]+)円', row_data.used_amount)
        if matches is None:
            raise ValueError(f'Invalid used amount. Used amount = {row_data.used_amount}')
        self.used_amount: int = int(matches.group(1).replace(',', ''))
        self.use_kind: Optional[WaonRow.UseKind] = WaonRow.UseKind(row_data.use_kind)
        self.charge_kind: Optional[WaonRow.ChargeKind] = self._convert_charge_kind_to_enum(row_data.charge_kind)

    @staticmethod
    def _convert_charge_kind_to_enum(charge_kind_string) -> Optional[WaonRow.ChargeKind]:
        if charge_kind_string == '-':
            return None
        try:
            return WaonRow.ChargeKind(charge_kind_string)
        except ValueError as error:
            raise ValueError(
                'The value of "Charge kind" has not been defined in this code. Charge kind =' + charge_kind_string
            ) from error

    def validate(self) -> ValidatedInputStoreRow:
        if self.use_kind is None:
            raise InvalidRowError(
                f'The value of "Use kind" has not been defined in this code. Use kind = {self.data.use_kind}'
            )
        return super().validate()

    def is_row_to_skip(self, store: Store) -> bool:
        """This property returns whether this row should be skipped or not."""
        return self.is_download_point

    @property
    def is_payment(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.use_kind == WaonRow.UseKind.PAYMENT

    @property
    def is_charge(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.use_kind == WaonRow.UseKind.CHARGE

    @property
    def is_charge_by_point(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.is_charge and self.charge_kind == WaonRow.ChargeKind.POINT

    @property
    def is_charge_by_bank_account(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.is_charge and self.charge_kind == WaonRow.ChargeKind.BANK_ACCOUNT

    @property
    def is_auto_charge(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.use_kind == WaonRow.UseKind.AUTO_CHARGE

    @property
    def is_download_point(self) -> bool:
        # Reason: Raw code is simple enough. pylint: disable=missing-docstring
        return self.use_kind == WaonRow.UseKind.DOWNLOAD_POINT


class WaonRowFactory(InputRowFactory):
    """This class implements factory to create WAON CSV row instance."""
    def create(self, account_id: AccountId, row_data: WaonRowData) -> WaonRow:
        return WaonRow(account_id, row_data)
