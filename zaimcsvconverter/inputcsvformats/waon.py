"""This module implements row model of WAON CSV."""
from __future__ import annotations
from abc import abstractmethod
from datetime import datetime
from enum import Enum
import re
from typing import TYPE_CHECKING, Type, Dict
from dataclasses import dataclass

from zaimcsvconverter import CONFIG
from zaimcsvconverter.input_row import InputStoreRowData, InputRowFactory, InputStoreRow
from zaimcsvconverter.models import Store
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
                f'The value of "Use kind" has not been defined in this code. Use kind = {row_data.use_kind}'
            ) from error

        waon_row_class = self.get_appropriate_row_class(use_kind)

        return waon_row_class(account, row_data)

    @staticmethod
    def get_appropriate_row_class(use_kind: WaonRow.UseKind) -> Type[WaonRow]:
        """This method returns appropriate row class."""
        dictionary_waon_row = {
            WaonRow.UseKind.PAYMENT: WaonPaymentRow,
            WaonRow.UseKind.CHARGE: WaonChargeRow,
            WaonRow.UseKind.AUTO_CHARGE: WaonAutoChargeRow,
            WaonRow.UseKind.DOWNLOAD_POINT: WaonDownloadPointRow,
        }
        waon_row_class = dictionary_waon_row.get(use_kind)
        if waon_row_class is None:
            raise ValueError(f'The mufg_row_class for {use_kind} has not been defined in this code.')
        return waon_row_class


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
        if matches is None:
            raise ValueError(f'Invalid used amount. Used amount = {row_data.used_amount}')
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
    def zaim_row_class_to_convert(self, store: Store) -> Type['ZaimRow']:
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
    def zaim_row_class_to_convert(self, store: Store) -> Type['ZaimPaymentRow']:
        return ZaimPaymentRow


class WaonChargeRow(WaonRow):
    """
    This class implements auto charge row model of WAON.
    """
    def zaim_row_class_to_convert(self, store: Store) -> Type['ZaimRow']:
        dictionary_zaim_row: Dict[WaonRow.ChargeKind, Type[ZaimRow]] = {
            WaonRow.ChargeKind.POINT: ZaimIncomeRow,
            WaonRow.ChargeKind.BANK_ACCOUNT: ZaimTransferRow,
        }
        zaim_row_class = dictionary_zaim_row.get(self._charge_kind)
        if zaim_row_class is None:
            raise ValueError(f'{WaonRow.ChargeKind} is not registered into dictionary_zaim_row.')
        return zaim_row_class


class WaonAutoChargeRow(WaonRow):
    """
    This class implements auto charge row model of WAON.
    """
    def zaim_row_class_to_convert(self, store: Store) -> Type['ZaimTransferRow']:
        return ZaimTransferRow


class WaonDownloadPointRow(WaonRow):
    """
    This class implements auto charge row model of WAON.
    """
    def zaim_row_class_to_convert(self, store: Store) -> Type['ZaimTransferRow']:
        raise ValueError("WAON download point row is only history data. It's no need to import into Zaim.")

    def is_row_to_skip(self, store: Store) -> bool:
        """This property returns whether this row should be skipped or not."""
        return True
