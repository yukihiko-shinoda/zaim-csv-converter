#!/usr/bin/env python

"""
This module implements row model of WAON CSV.
"""

from __future__ import annotations
from abc import abstractmethod
import datetime
from enum import Enum
import re
from typing import TYPE_CHECKING
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.input_row import InputStoreRowData, InputRowFactory, InputStoreRow
from zaimcsvconverter.zaim_row import ZaimRow, ZaimPaymentRow, ZaimTransferRow, ZaimIncomeRow

if TYPE_CHECKING:
    from zaimcsvconverter.account import Account


class WaonRowFactory(InputRowFactory):
    """This class implements factory to create WAON CSV row instance."""
    def create(self, account: 'Account', row_data: WaonRowData) -> WaonRow:
        try:
            use_kind = WaonRow.UseKind(row_data.use_kind)
        except ValueError as error:
            raise ValueError(
                'The value of "Use kind" has not been defined in this code. Use kind =' + row_data.use_kind
            ) from error

        waon_row_class = {
            WaonRow.UseKind.PAYMENT: WaonPaymentRow,
            WaonRow.UseKind.CHARGE: WaonChargeRow,
            WaonRow.UseKind.AUTO_CHARGE: WaonAutoChargeRow,
            WaonRow.UseKind.DOWNLOAD_POINT: WaonDownloadPointRow,
        }.get(use_kind)

        return waon_row_class(account, row_data)


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
        """This property returns date as datetime."""
        return datetime.datetime.strptime(self._date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        """This property returns store name."""
        return self._used_store


class WaonRow(InputStoreRow):
    """This class implements row model of WAON CSV."""
    class UseKind(Enum):
        """This class implements constant of user kind in WAON CSV."""
        PAYMENT: str = '支払'
        CHARGE: str = 'チャージ'
        AUTO_CHARGE: str = 'オートチャージ'
        DOWNLOAD_POINT: str = 'ポイントダウンロード'

    class ChargeKind(Enum):
        """This class implements constant of charge kind in WAON CSV."""
        BANK_ACCOUNT: str = '銀行口座'
        POINT: str = 'ポイント'

    def __init__(self, account: 'Account', row_data: WaonRowData):
        super().__init__(account, row_data)
        matches = re.search(r'([\d,]+)円', row_data.used_amount)
        self._used_amount: int = int(matches.group(1).replace(',', ''))
        self._charge_kind: WaonRow.ChargeKind = self._convert_charge_kind_to_enum(row_data.charge_kind)

    @staticmethod
    def _convert_charge_kind_to_enum(charge_kind_string):
        if charge_kind_string == '-':
            return None
        try:
            return WaonRow.ChargeKind(charge_kind_string)
        except ValueError as error:
            raise ValueError(
                'The value of "Charge kind" has not been defined in this code. Charge kind =' + charge_kind_string
            ) from error

    @abstractmethod
    def convert_to_zaim_row(self) -> ZaimRow:
        pass

    @property
    def zaim_income_cash_flow_target(self) -> str:
        return CONFIG.waon.account_name

    @property
    def zaim_income_ammount_income(self) -> int:
        return self._used_amount

    @property
    def zaim_payment_cash_flow_source(self) -> str:
        return CONFIG.waon.account_name

    @property
    def zaim_payment_amount_payment(self) -> int:
        return self._used_amount

    @property
    def zaim_transfer_cash_flow_source(self) -> str:
        return CONFIG.waon.auto_charge_source

    @property
    def zaim_transfer_cash_flow_target(self) -> str:
        return CONFIG.waon.account_name

    @property
    def zaim_transfer_amount_transfer(self) -> int:
        return self._used_amount


class WaonPaymentRow(WaonRow):
    """
    This class implements payment row model of WAON.
    """
    def convert_to_zaim_row(self) -> ZaimPaymentRow:
        return ZaimPaymentRow(self)


class WaonChargeRow(WaonRow):
    """
    This class implements auto charge row model of WAON.
    """
    def convert_to_zaim_row(self) -> ZaimTransferRow:
        zaim_row_class = {
            WaonRow.ChargeKind.POINT: ZaimIncomeRow,
            WaonRow.ChargeKind.BANK_ACCOUNT: ZaimTransferRow,
        }.get(self._charge_kind)

        return zaim_row_class(self)


class WaonAutoChargeRow(WaonRow):
    """
    This class implements auto charge row model of WAON.
    """
    def convert_to_zaim_row(self) -> ZaimTransferRow:
        return ZaimTransferRow(self)


class WaonDownloadPointRow(WaonRow):
    """
    This class implements auto charge row model of WAON.
    """
    def convert_to_zaim_row(self) -> ZaimTransferRow:
        raise ValueError('WAON download point row is only history data. It\'s no need to import into Zaim.')

    @property
    def is_row_to_skip(self) -> bool:
        """This property returns whether this row should be skipped or not."""
        return True
