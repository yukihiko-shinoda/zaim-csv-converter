#!/usr/bin/env python

"""
This module implements abstract row model of Zaim CSV.
"""

import datetime
from abc import ABCMeta, abstractmethod
from typing import List

from zaimcsvconverter.models import Store, Item
from zaimcsvconverter.input_row import InputRow


# pylint: disable=too-many-instance-attributes
class ZaimRow(metaclass=ABCMeta):
    """
    This class implements abstract row model of Zaim CSV.
    """
    CATEGORY_LARGE_EMPTY = '-'
    CATEGORY_SMALL_EMPTY = '-'
    CASH_FLOW_SOURCE_EMPTY = ''
    CASH_FLOW_TARGET_EMPTY = ''
    AMOUNT_INCOME_EMPTY = 0
    AMOUNT_PAYMENT_EMPTY = 0
    AMOUNT_TRANSFER_EMPTY = 0
    STORE_NAME_EMPTY = ''
    ITEM_NAME_EMPTY = ''
    NOTE_EMPTY = ''
    CURRENCY_EMPTY = ''
    BALANCE_ADJUSTMENT_EMPTY = ''
    AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY = ''
    SETTING_AGGREGATE_EMPTY = ''

    @property
    def _date_string(self) -> str:
        return self._date.strftime("%Y-%m-%d")

    def __init__(self, input_row: InputRow):
        self._date: datetime = input_row.zaim_date
        self._store: Store = input_row.zaim_store
        self._item: Item = input_row.zaim_item

    @abstractmethod
    def convert_to_list(self) -> List[str]:
        """
        This method converts object data to list.
        """
        pass


class ZaimIncomeRow(ZaimRow):
    """
    This class implements income row model of Zaim CSV.
    """
    METHOD: str = 'income'

    def __init__(self, input_row: InputRow):
        self._cash_flow_target: str = input_row.zaim_income_cash_flow_target
        self._amount_income: int = input_row.zaim_income_ammount_income
        super().__init__(input_row)

    def convert_to_list(self) -> List[str]:
        return [
            self._date_string,
            self.METHOD,
            self._store.category_income,
            self.CATEGORY_SMALL_EMPTY,
            self.CASH_FLOW_SOURCE_EMPTY,
            self._cash_flow_target,
            self.ITEM_NAME_EMPTY,
            self.NOTE_EMPTY,
            self._store.name_zaim,
            self.CURRENCY_EMPTY,
            self._amount_income,
            self.AMOUNT_PAYMENT_EMPTY,
            self.AMOUNT_TRANSFER_EMPTY,
            self.BALANCE_ADJUSTMENT_EMPTY,
            self.AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY,
            self.SETTING_AGGREGATE_EMPTY
        ]


class ZaimPaymentRow(ZaimRow):
    """
    This class implements payment row model of Zaim CSV.
    """
    METHOD: str = 'payment'

    def __init__(self, input_row: InputRow):
        self._cash_flow_source: str = input_row.zaim_payment_cash_flow_source
        self._note: int = input_row.zaim_payment_note
        self._amount_payment: int = input_row.zaim_payment_amount_payment
        super().__init__(input_row)

    def convert_to_list(self) -> List[str]:
        return [
            self._date_string,
            self.METHOD,
            self._item.category_payment_large if self._item is not None else self._store.category_payment_large,
            self._item.category_payment_small if self._item is not None else self._store.category_payment_small,
            self._cash_flow_source,
            self.CASH_FLOW_TARGET_EMPTY,
            self._item.name if self._item is not None else None,
            self._note,
            self._store.name_zaim,
            self.CURRENCY_EMPTY,
            self.AMOUNT_INCOME_EMPTY,
            self._amount_payment,
            self.AMOUNT_TRANSFER_EMPTY,
            self.BALANCE_ADJUSTMENT_EMPTY,
            self.AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY,
            self.SETTING_AGGREGATE_EMPTY
        ]


class ZaimTransferRow(ZaimRow):
    """
    This class implements transfer row model of Zaim CSV.
    """
    METHOD: str = 'transfer'

    def __init__(self, input_row: InputRow):
        self._cash_flow_source: str = input_row.zaim_transfer_cash_flow_source
        self._cash_flow_target: str = input_row.zaim_transfer_cash_flow_target
        self._amount_transfer: int = input_row.zaim_transfer_amount_transfer
        super().__init__(input_row)

    def convert_to_list(self) -> List[str]:
        return [
            self._date_string,
            self.METHOD,
            self.CATEGORY_LARGE_EMPTY,
            self.CATEGORY_SMALL_EMPTY,
            self._cash_flow_source,
            self._cash_flow_target,
            self.ITEM_NAME_EMPTY,
            self.NOTE_EMPTY,
            self.STORE_NAME_EMPTY,
            self.CURRENCY_EMPTY,
            self.AMOUNT_INCOME_EMPTY,
            self.AMOUNT_PAYMENT_EMPTY,
            self._amount_transfer,
            self.BALANCE_ADJUSTMENT_EMPTY,
            self.AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY,
            self.SETTING_AGGREGATE_EMPTY
        ]
