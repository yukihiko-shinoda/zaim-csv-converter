#!/usr/bin/env python
import datetime
from abc import ABCMeta, abstractmethod
from typing import NoReturn, List

from zaimcsvconverter.models import Store
from zaimcsvconverter.mufg.mufg_row import MufgRow
from zaimcsvconverter.waon.waon_row import WaonRow

from zaimcsvconverter.account_row import AccountRow
from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_row import GoldPointCardPlusRow


# pylint: disable=too-many-instance-attributes
class ZaimRow(metaclass=ABCMeta):
    CATEGORY_LARGE_EMPTY = '-'
    CATEGORY_SMALL_EMPTY = '-'
    CASH_FLOW_SOURCE_EMPTY = ''
    CASH_FLOW_TARGET_EMPTY = ''
    AMOUNT_INCOME_EMPTY = 0
    AMOUNT_PAYMENT_EMPTY = 0
    AMOUNT_TRANSFER_EMPTY = 0
    ITEM_NAME_EMPTY = ''
    NOTE_NAME_EMPTY = ''
    CURRENCY_EMPTY = ''
    BALANCE_ADJUSTMENT_EMPTY = ''
    AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY = ''
    SETTING_AGGREGATE_EMPTY = ''

    @property
    def _category_large(self) -> str:
        return self.__category_large

    @_category_large.setter
    def _category_large(self, category_large: str):
        self.__category_large: str = category_large

    @property
    def _category_small(self) -> str:
        return self.__category_small

    @_category_small.setter
    def _category_small(self, category_small: str):
        self.__category_small: str = category_small

    @property
    def _cash_flow_source(self) -> str:
        return self.__cash_flow_source

    @_cash_flow_source.setter
    def _cash_flow_source(self, cash_flow_source: str):
        self.__cash_flow_source: str = cash_flow_source

    @property
    def _cash_flow_target(self) -> str:
        return self.__cash_flow_target

    @_cash_flow_target.setter
    def _cash_flow_target(self, cash_flow_target: str):
        self.__cash_flow_target: str = cash_flow_target

    @property
    def _store(self) -> Store:
        return self.__store

    @_store.setter
    def _store(self, store: Store):
        self.__store: Store = store

    @property
    def _amount_income(self) -> int:
        return self.__amount_income

    @_amount_income.setter
    def _amount_income(self, amount_income: int):
        self.__amount_income: int = amount_income

    @property
    def _amount_payment(self) -> int:
        return self.__amount_payment

    @_amount_payment.setter
    def _amount_payment(self, amount_payment: int):
        self.__amount_payment: int = amount_payment

    @property
    def _amount_transfer(self) -> int:
        return self.__amount_transfer

    @_amount_transfer.setter
    def _amount_transfer(self, amount_transfer: int):
        self.__amount_transfer: int = amount_transfer

    def __init__(self, account_row: AccountRow, method: str):
        self._method = method
        if isinstance(account_row, WaonRow):
            self._initialize_by_waon_row(account_row)
        elif isinstance(account_row, GoldPointCardPlusRow):
            self._initialize_by_gold_point_card_plus_row(account_row)
        elif isinstance(account_row, MufgRow):
            self._initialize_by_mufg_row(account_row)
        else:
            raise TypeError('Argument "row" is unsupported instance type. Type = ' + type(account_row).__name__)

    def _initialize_by_account_row_common(self, date: datetime) -> NoReturn:
        self._date: datetime = date

    @abstractmethod
    def convert_to_list(self) -> List[str]:
        pass

    @abstractmethod
    def _initialize_by_waon_row(self, waon_row: WaonRow) -> NoReturn:
        self._date: datetime = waon_row.date
        self._store: Store = waon_row.used_store

    @abstractmethod
    def _initialize_by_gold_point_card_plus_row(self, gold_point_card_plus_row: GoldPointCardPlusRow) -> NoReturn:
        self._date: datetime = gold_point_card_plus_row.used_date
        self._store: Store = gold_point_card_plus_row.used_store

    @abstractmethod
    def _initialize_by_mufg_row(self, mufg_row: MufgRow) -> NoReturn:
        self._date: datetime = mufg_row.date
        self._store: Store = mufg_row.summary_content
