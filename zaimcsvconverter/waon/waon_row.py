#!/usr/bin/env python

"""
This module implements row model of WAON CSV.
"""

from __future__ import annotations
from abc import abstractmethod
import datetime
from enum import Enum
import re
from dataclasses import dataclass
from zaimcsvconverter import CONFIG
from zaimcsvconverter.account_row import AccountRow, AccountRowData
from zaimcsvconverter.enum import Account
from zaimcsvconverter.models import Store
from zaimcsvconverter.zaim.zaim_row import ZaimRow, ZaimPaymentRow, ZaimTransferRow


@dataclass
class WaonRowData(AccountRowData):
    """This class implements data class for wrapping list of WAON CSV row model."""
    date: str
    used_store: str
    used_amount: str
    use_kind: str
    charge_kind: str


class WaonRow(AccountRow):
    """
    This class implements row model of WAON CSV.
    """
    class UseKind(Enum):
        """
        This class implements constant of user kind in WAON CSV.
        """
        PAYMENT: str = '支払'
        AUTO_CHARGE: str = 'オートチャージ'

    def __init__(self, row_data: WaonRowData):
        self._date: datetime = datetime.datetime.strptime(row_data.date, "%Y/%m/%d")
        self._used_store: Store = Store.try_to_find(Account.WAON, row_data.used_store)
        matches = re.search(r'([\d,]+)円', row_data.used_amount)
        self._used_amount: int = int(matches.group(1).replace(',', ''))
        self._charge_kind: str = row_data.charge_kind

    @abstractmethod
    def convert_to_zaim_row(self) -> ZaimRow:
        pass

    @property
    def zaim_date(self) -> datetime:
        return self._date

    @property
    def zaim_store(self) -> Store:
        return self._used_store

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

    @staticmethod
    def create(row_data: WaonRowData) -> WaonRow:
        try:
            use_kind = WaonRow.UseKind(row_data.use_kind)
        except ValueError as error:
            raise ValueError(
                'The value of "Use kind" has not been defined in this code. Use kind =' + row_data.use_kind
            ) from error

        return {
            WaonRow.UseKind.PAYMENT: WaonPaymentRow(row_data),
            WaonRow.UseKind.AUTO_CHARGE: WaonAutoChargeRow(row_data)
        }.get(use_kind)


class WaonPaymentRow(WaonRow):
    """
    This class implements payment row model of WAON.
    """
    def convert_to_zaim_row(self) -> ZaimPaymentRow:
        return ZaimPaymentRow(self)


class WaonAutoChargeRow(WaonRow):
    """
    This class implements auto charge row model of WAON.
    """
    def convert_to_zaim_row(self) -> ZaimTransferRow:
        return ZaimTransferRow(self)
