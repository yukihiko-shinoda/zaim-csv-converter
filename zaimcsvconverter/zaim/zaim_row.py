#!/usr/bin/env python
from abc import ABCMeta, abstractmethod
from typing import NoReturn

from zaimcsvconverter.session_manager import SessionManager
from zaimcsvconverter.waon.waon_row import WaonRow


class ZaimRow(metaclass=ABCMeta):
    # INDEX_DATE = 0
    # INDEX_METHOD = 1
    # INDEX_CATEGORY_LARGE = 2
    # INDEX_CATEGORY_SMALL = 3
    # INDEX_CASH_FLOW_SOURCE = 4
    # INDEX_CASH_FLOW_TARGET = 5
    # INDEX_ITEM_NAME = 6
    # INDEX_NOTE = 7
    # INDEX_STORE = 8
    # INDEX_CURRENCY = 9
    # INDEX_AMOUNT_INCOME = 10
    # INDEX_AMOUNT_PAYMENT = 11
    # INDEX_AMOUNT_TRANSFER = 12
    # INDEX_BALANCE_ADJUSTMENT = 13
    # INDEX_AMOUNT_BEFORE_CURRENCY_CONVERSION = 14
    # INDEX_SETTING_AGGREGATE = 15
    ACCOUNT_WAON = 'WAON'
    ACCOUNT_AEON_BANK = 'イオン銀行'

    @property
    def _category_large(self):
        return self.__category_large

    @_category_large.setter
    def _category_large(self, category_large):
        self.__category_large = category_large

    @property
    def _category_small(self):
        return self.__category_small

    @_category_small.setter
    def _category_small(self, category_small):
        self.__category_small = category_small

    @property
    def _cash_flow_source(self):
        return self.__cash_flow_source

    @_cash_flow_source.setter
    def _cash_flow_source(self, cash_flow_source):
        self.__cash_flow_source = cash_flow_source

    @property
    def _cash_flow_target(self):
        return self.__cash_flow_target

    @_cash_flow_target.setter
    def _cash_flow_target(self, cash_flow_target):
        self.__cash_flow_target = cash_flow_target

    @property
    def _store(self):
        return self.__store

    @_store.setter
    def _store(self, store):
        self.__store = store

    @property
    def _amount_income(self):
        return self.__amount_income

    @_amount_income.setter
    def _amount_income(self, amount_income):
        self.__amount_income = amount_income

    @property
    def _amount_payment(self):
        return self.__amount_payment

    @_amount_payment.setter
    def _amount_payment(self, amount_payment):
        self.__amount_payment = amount_payment

    @property
    def _amount_transfer(self):
        return self.__amount_transfer

    @_amount_transfer.setter
    def _amount_transfer(self, amount_transfer):
        self.__amount_transfer = amount_transfer

    def __init__(self, row, database_wrapper):
        if isinstance(row, WaonRow):
            self._initialize_by_waon_row(row, database_wrapper)
        else:
            raise TypeError('Argument "row" is unsupported instance type. Type = ' + type(row).__name__)

    @abstractmethod
    def get_method(self):
        pass

    @abstractmethod
    def _initialize_by_waon_row(self, waon_row: WaonRow, session_manager: SessionManager) -> NoReturn:
        pass

    def _initialize_by_waon_row_common(self, waon_row: WaonRow) -> NoReturn:
        self._date = waon_row.date
        self._item_name = ''
        self._note = ''
        self._currency = ''
        self._balance_adjustment = ''
        self._amount_before_currency_conversion = ''
        self._setting_aggregate = ''

    def convert_to_list(self):
        list_row_zaim = []
        list_row_zaim.append(self._date.strftime("%Y-%m-%d"))
        list_row_zaim.append(self.get_method())
        list_row_zaim.append(self._category_large)
        list_row_zaim.append(self._category_small)
        list_row_zaim.append(self._cash_flow_source)
        list_row_zaim.append(self._cash_flow_target)
        list_row_zaim.append(self._item_name)
        list_row_zaim.append(self._note)
        list_row_zaim.append(self._store)
        list_row_zaim.append(self._currency)
        list_row_zaim.append(self._amount_income)
        list_row_zaim.append(self._amount_payment)
        list_row_zaim.append(self._amount_transfer)
        list_row_zaim.append(self._balance_adjustment)
        list_row_zaim.append(self._amount_before_currency_conversion)
        list_row_zaim.append(self._setting_aggregate)

        return list_row_zaim
