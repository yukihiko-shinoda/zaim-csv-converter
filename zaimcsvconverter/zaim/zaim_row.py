#!/usr/bin/env python
from abc import ABCMeta, abstractmethod
from typing import NoReturn

from sqlalchemy.orm.exc import NoResultFound

from zaimcsvconverter import CONFIG
from zaimcsvconverter.goldpointcardplus.gold_point_card_plus_row import GoldPointCardPlusRow
from zaimcsvconverter.models import Store
from zaimcsvconverter.session_manager import SessionManager
from zaimcsvconverter.waon.waon_row import WaonRow
from zaimcsvconverter.zaim_csv_converter import ZaimCsvConverter


class ZaimRow(metaclass=ABCMeta):
    ACCOUNT_CREDIT_CARD = 'クレジットカード'

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

    def __init__(self, account_row, method):
        self._method = method
        if isinstance(account_row, WaonRow):
            self._initialize_by_waon_row(account_row)
        elif isinstance(account_row, GoldPointCardPlusRow):
            self._initialize_by_gold_point_card_plus_row(account_row)
        else:
            raise TypeError('Argument "row" is unsupported instance type. Type = ' + type(account_row).__name__)

    def _initialize_by_waon_row_common(self, waon_row: WaonRow) -> NoReturn:
        self._date = waon_row.date
        self._item_name = ''
        self._note = ''
        self._currency = ''
        self._balance_adjustment = ''
        self._amount_before_currency_conversion = ''
        self._setting_aggregate = ''

    def convert_to_list(self):
        list_row_zaim = [
            self._date.strftime("%Y-%m-%d"),
            self._method,
            self._category_large,
            self._category_small,
            self._cash_flow_source,
            self._cash_flow_target,
            self._item_name,
            self._note,
            self._store,
            self._currency,
            self._amount_income,
            self._amount_payment,
            self._amount_transfer,
            self._balance_adjustment,
            self._amount_before_currency_conversion,
            self._setting_aggregate
        ]

        return list_row_zaim

    @abstractmethod
    def _initialize_by_waon_row(self, waon_row: WaonRow) -> NoReturn:
        pass

    def _initialize_by_gold_point_card_plus_row(self, gold_point_card_plus_row: GoldPointCardPlusRow) -> NoReturn:
        store = self._try_to_find_gold_point_card_plus_store(gold_point_card_plus_row)
        self._date = gold_point_card_plus_row.used_date
        self._category_large = store.category_large
        self._category_small = store.category_small
        self._cash_flow_source = CONFIG.gold_point_card_plus.account_name
        self._cash_flow_target = '-'
        self._item_name = ''
        self._note = ''
        self._store = store.name_zaim
        self._currency = ''
        self._amount_income = 0
        self._amount_payment = gold_point_card_plus_row.used_amount
        self._amount_transfer = 0
        self._balance_adjustment = ''
        self._amount_before_currency_conversion = ''
        self._setting_aggregate = ''

    @staticmethod
    def _try_to_find_waon_store(waon_row):
        return ZaimRow.method_name(
            Store.STORE_KIND_WAON,
            waon_row.used_store,
            ZaimCsvConverter.FILE_CSV_CONVERT_WAON)

    @staticmethod
    def _try_to_find_gold_point_card_plus_store(gold_point_card_plus_row):
        return ZaimRow.method_name(
            Store.STORE_KIND_GOLD_POINT_CARD_PLUS,
            gold_point_card_plus_row.used_store,
            ZaimCsvConverter.FILE_CSV_CONVERT_GOLD_POINT_CARD_PLUS)

    @staticmethod
    def method_name(store_kind, use_store, file_csv_convert):
        try:
            with SessionManager() as session_manager:
                return session_manager.find_store(store_kind, use_store)
        except NoResultFound as e:
            raise KeyError(
                f'"{use_store}" is not defined on {file_csv_convert}. ' + 'Please define it.'
            ) from e
