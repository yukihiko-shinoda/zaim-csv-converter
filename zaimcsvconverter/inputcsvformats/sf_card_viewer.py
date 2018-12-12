#!/usr/bin/env python

"""
This module implements row model of SF Card Viewer CSV.
"""

from __future__ import annotations
import datetime
from abc import abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Callable
from dataclasses import dataclass

from zaimcsvconverter.input_row import InputStoreRowData, InputRowFactory, InputStoreRow
from zaimcsvconverter.config import SFCardViewerConfig
if TYPE_CHECKING:
    from zaimcsvconverter.account import Account
    from zaimcsvconverter.zaim_row import ZaimPaymentRow
    from zaimcsvconverter.zaim_row import ZaimTransferRow


class SFCardViewerRowFactory(InputRowFactory):
    """This class implements factory to create WAON CSV row instance."""
    def __init__(self, account_config: Callable[[], SFCardViewerConfig]):
        self._account_config = account_config

    def create(self, account: 'Account', row_data: SFCardViewerRowData) -> SFCardViewerRow:
        try:
            note = Note(row_data.note)
        except ValueError as error:
            raise ValueError(
                f'The value of "Note" has not been defined in this code. Note = {row_data.note}'
            ) from error

        sf_card_viewer_row_class = {
            Note.EMPTY: SFCardViewerTransportationRow,
            Note.SALES_GOODS: SFCardViewerSalesGoodsRow,
            Note.AUTO_CHARGE: SFCardViewerAutoChargeRow,
            Note.EXIT_BY_WINDOW: SFCardViewerExitByWindowRow,
        }.get(note)

        return sf_card_viewer_row_class(account, row_data, self._account_config())


class Note(Enum):
    """
    This class implements constant of note in SF Card Viewer CSV.
    """
    EMPTY: str = ''
    SALES_GOODS: str = '物販'
    AUTO_CHARGE: str = 'ｵｰﾄﾁｬｰｼﾞ'
    EXIT_BY_WINDOW: str = '窓出'


@dataclass
class SFCardViewerRowData(InputStoreRowData):
    """This class implements data class for wrapping list of SF Card Viewer CSV row model."""
    _used_date: str
    is_commuter_pass_enter: str
    railway_company_name_enter: str
    station_name_enter: str
    is_commuter_pass_exit: str
    railway_company_name_exit: str
    _station_name_exit: str
    used_amount: str
    balance: str
    note: str

    @property
    def date(self) -> datetime:
        """This property returns date as datetime."""
        return datetime.datetime.strptime(self._used_date, "%Y/%m/%d")

    @property
    def store_name(self) -> str:
        """This property returns store name."""
        return self._station_name_exit


# pylint: disable=too-many-instance-attributes
class SFCardViewerRow(InputStoreRow):
    """
    This class implements row model of SF Card Viewer CSV.
    """
    def __init__(self, account: 'Account', row_data: SFCardViewerRowData, account_config: SFCardViewerConfig):
        super().__init__(account, row_data)
        self._is_commuter_pass_enter: str = row_data.is_commuter_pass_enter
        self._railway_company_name_enter: str = row_data.railway_company_name_enter
        self._station_name_enter: str = row_data.station_name_enter
        self._is_commuter_pass_exit: str = row_data.is_commuter_pass_exit
        self._railway_company_name_exit: str = row_data.railway_company_name_exit
        self._used_amount: int = int(row_data.used_amount)
        self._balance: int = int(row_data.balance)
        self._note: str = str(row_data.note)
        self._account_config: SFCardViewerConfig = account_config

    @abstractmethod
    def convert_to_zaim_row(self) -> 'ZaimPaymentRow':
        pass

    @property
    def zaim_income_cash_flow_target(self) -> str:
        raise ValueError('Income row for SF Card Viewer is not defined. Please confirm CSV file.')

    @property
    def zaim_income_ammount_income(self) -> int:
        raise ValueError('Income row for SF Card Viewer is not defined. Please confirm CSV file.')

    @property
    def zaim_payment_cash_flow_source(self) -> str:
        return self._account_config.account_name

    @property
    def zaim_payment_note(self) -> str:
        if self.zaim_store is None:
            return ''
        return f'{self._railway_company_name_enter} {self._station_name_enter}' \
               + f' → {self._railway_company_name_exit} {self.zaim_store.name}'

    @property
    def zaim_payment_amount_payment(self) -> int:
        return self._used_amount

    @property
    def zaim_transfer_cash_flow_source(self) -> str:
        return self._account_config.auto_charge_source

    @property
    def zaim_transfer_cash_flow_target(self) -> str:
        return self._account_config.account_name

    @property
    def zaim_transfer_amount_transfer(self) -> int:
        return -1 * self._used_amount


class SFCardViewerTransportationRow(SFCardViewerRow):
    """This class implements transportation row model of SF Card Viewer CSV."""
    def convert_to_zaim_row(self) -> 'ZaimPaymentRow':
        from zaimcsvconverter.zaim_row import ZaimPaymentRow
        return ZaimPaymentRow(self)


class SFCardViewerSalesGoodsRow(SFCardViewerRow):
    """This class implements sales goods row model of SF Card Viewer CSV."""
    @property
    def is_row_to_skip(self) -> bool:
        return self._account_config.skip_sales_goods_row

    def convert_to_zaim_row(self) -> 'ZaimPaymentRow':
        from zaimcsvconverter.zaim_row import ZaimPaymentRow
        return ZaimPaymentRow(self)


class SFCardViewerAutoChargeRow(SFCardViewerRow):
    """This class implements auto charge row model of SF Card Viewer CSV."""
    def convert_to_zaim_row(self) -> 'ZaimTransferRow':
        from zaimcsvconverter.zaim_row import ZaimTransferRow
        return ZaimTransferRow(self)


class SFCardViewerExitByWindowRow(SFCardViewerRow):
    """This class implements exit by window row model of SF Card Viewer CSV."""
    @property
    def is_row_to_skip(self) -> bool:
        return self._used_amount == 0 and \
               self._railway_company_name_enter == self._railway_company_name_exit and \
               self._station_name_enter == self.zaim_store.name

    def convert_to_zaim_row(self) -> 'ZaimPaymentRow':
        from zaimcsvconverter.zaim_row import ZaimPaymentRow
        return ZaimPaymentRow(self)
