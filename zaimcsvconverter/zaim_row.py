"""This module implements abstract row model of Zaim CSV."""
from abc import abstractmethod
from typing import List, Union, Optional

from datetime import datetime

from zaimcsvconverter.models import Store, Item
from zaimcsvconverter.inputcsvformats import ValidatedInputRow, ValidatedInputItemRow


# pylint: disable=too-many-instance-attributes
class ZaimRow:
    """This class implements abstract row model of Zaim CSV."""
    HEADER = [
        '日付',
        '方法',
        'カテゴリ',
        'カテゴリの内訳',
        '支払元',
        '入金先',
        '品目',
        'メモ',
        'お店',
        '通貨',
        '収入',
        '支出',
        '振替',
        '残高調整',
        '通貨変換前の金額',
        '集計の設定'
    ]
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

    def __init__(self, validated_input_row: ValidatedInputRow):
        input_row = validated_input_row.input_row
        self._date: datetime = input_row.zaim_date
        self._store: Store = validated_input_row.store
        self._item: Optional[Item] = \
            validated_input_row.item if isinstance(validated_input_row, ValidatedInputItemRow) else None

    @abstractmethod
    def convert_to_list(self) -> List[Optional[Union[str, int]]]:
        """This method converts object data to list."""


class ZaimIncomeRow(ZaimRow):
    """This class implements income row model of Zaim CSV."""
    METHOD: str = 'income'

    def __init__(self, validated_input_row: ValidatedInputRow, cash_flow_target: str, amount_income: int):
        self._cash_flow_target = cash_flow_target
        self._amount_income = amount_income
        super().__init__(validated_input_row)

    def convert_to_list(self) -> List[Optional[Union[str, int]]]:
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
    """This class implements payment row model of Zaim CSV."""
    METHOD: str = 'payment'

    def __init__(self, validated_input_row: ValidatedInputRow, cash_flow_source: str, note: str, amount_payment: int):
        self._cash_flow_source = cash_flow_source
        self._note = note
        self._amount_payment = amount_payment
        super().__init__(validated_input_row)

    def convert_to_list(self) -> List[Optional[Union[str, int]]]:
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
    """This class implements transfer row model of Zaim CSV."""
    METHOD: str = 'transfer'

    def __init__(
            self,
            validated_input_row: ValidatedInputRow,
            cash_flow_source: str,
            cash_flow_target: str,
            amount_transfer: int
    ):
        self._cash_flow_source: str = cash_flow_source
        self._cash_flow_target: str = cash_flow_target
        self._amount_transfer: int = amount_transfer
        super().__init__(validated_input_row)

    def convert_to_list(self) -> List[Optional[Union[str, int]]]:
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
