"""This module implements abstract row model of Zaim CSV."""
from abc import abstractmethod
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING, Union

from zaimcsvconverter.inputcsvformats import InputRow, InputRowData
from zaimcsvconverter.inputtooutput.exporters import OutputRecord
from zaimcsvconverter.inputtooutput.exporters.zaim.csv.zaim_csv_format import ZaimCsvFormat

if TYPE_CHECKING:
    from zaimcsvconverter.inputtooutput.converters.recordtozaim import (
        ZaimIncomeRowConverter,
        ZaimPaymentRowConverter,
        ZaimRowConverter,
        ZaimTransferRowConverter,
    )


class ZaimRow(OutputRecord):
    """This class implements abstract row model of Zaim CSV."""

    def __init__(self, zaim_row_converter: "ZaimRowConverter[InputRow[InputRowData], InputRowData]"):
        self._date: datetime = zaim_row_converter.date

    @property
    def _date_string(self) -> str:
        return self._date.strftime("%Y-%m-%d")

    @abstractmethod
    def convert_to_list(self) -> List[Optional[Union[str, int]]]:
        """This method converts object data to list."""


class ZaimIncomeRow(ZaimRow):
    """This class implements income row model of Zaim CSV."""

    METHOD: str = "income"

    def __init__(self, zaim_row_converter: "ZaimIncomeRowConverter[InputRow[InputRowData], InputRowData]"):
        self._category = zaim_row_converter.category
        self._cash_flow_target = zaim_row_converter.cash_flow_target
        self._store_name = zaim_row_converter.store_name
        self._amount_income = zaim_row_converter.amount
        super().__init__(zaim_row_converter)

    def convert_to_list(self) -> List[Optional[Union[str, int]]]:
        return [
            self._date_string,
            self.METHOD,
            self._category,
            ZaimCsvFormat.CATEGORY_SMALL_EMPTY,
            ZaimCsvFormat.CASH_FLOW_SOURCE_EMPTY,
            self._cash_flow_target,
            ZaimCsvFormat.ITEM_NAME_EMPTY,
            ZaimCsvFormat.NOTE_EMPTY,
            self._store_name,
            ZaimCsvFormat.CURRENCY_EMPTY,
            self._amount_income,
            ZaimCsvFormat.AMOUNT_PAYMENT_EMPTY,
            ZaimCsvFormat.AMOUNT_TRANSFER_EMPTY,
            ZaimCsvFormat.BALANCE_ADJUSTMENT_EMPTY,
            ZaimCsvFormat.AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY,
            ZaimCsvFormat.SETTING_AGGREGATE_EMPTY,
        ]


class ZaimPaymentRow(ZaimRow):
    """This class implements payment row model of Zaim CSV."""

    METHOD: str = "payment"

    def __init__(self, zaim_row_converter: "ZaimPaymentRowConverter[InputRow[InputRowData], InputRowData]"):
        self._category_large = zaim_row_converter.category_large
        self._category_small = zaim_row_converter.category_small
        self._cash_flow_source = zaim_row_converter.cash_flow_source
        self._item_name = zaim_row_converter.item_name
        self._note = zaim_row_converter.note
        self._store_name = zaim_row_converter.store_name
        self._amount_payment = zaim_row_converter.amount
        super().__init__(zaim_row_converter)

    def convert_to_list(self) -> List[Optional[Union[str, int]]]:
        return [
            self._date_string,
            self.METHOD,
            self._category_large,
            self._category_small,
            self._cash_flow_source,
            ZaimCsvFormat.CASH_FLOW_TARGET_EMPTY,
            self._item_name,
            self._note,
            self._store_name,
            ZaimCsvFormat.CURRENCY_EMPTY,
            ZaimCsvFormat.AMOUNT_INCOME_EMPTY,
            self._amount_payment,
            ZaimCsvFormat.AMOUNT_TRANSFER_EMPTY,
            ZaimCsvFormat.BALANCE_ADJUSTMENT_EMPTY,
            ZaimCsvFormat.AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY,
            ZaimCsvFormat.SETTING_AGGREGATE_EMPTY,
        ]


class ZaimTransferRow(ZaimRow):
    """This class implements transfer row model of Zaim CSV."""

    METHOD: str = "transfer"

    def __init__(self, zaim_row_converter: "ZaimTransferRowConverter[InputRow[InputRowData], InputRowData]"):
        self._cash_flow_source: str = zaim_row_converter.cash_flow_source
        self._cash_flow_target: str = zaim_row_converter.cash_flow_target
        self._amount_transfer: int = zaim_row_converter.amount
        super().__init__(zaim_row_converter)

    def convert_to_list(self) -> List[Optional[Union[str, int]]]:
        return [
            self._date_string,
            self.METHOD,
            ZaimCsvFormat.CATEGORY_LARGE_EMPTY,
            ZaimCsvFormat.CATEGORY_SMALL_EMPTY,
            self._cash_flow_source,
            self._cash_flow_target,
            ZaimCsvFormat.ITEM_NAME_EMPTY,
            ZaimCsvFormat.NOTE_EMPTY,
            ZaimCsvFormat.STORE_NAME_EMPTY,
            ZaimCsvFormat.CURRENCY_EMPTY,
            ZaimCsvFormat.AMOUNT_INCOME_EMPTY,
            ZaimCsvFormat.AMOUNT_PAYMENT_EMPTY,
            self._amount_transfer,
            ZaimCsvFormat.BALANCE_ADJUSTMENT_EMPTY,
            ZaimCsvFormat.AMOUNT_BEFORE_CURRENCY_CONVERSION_EMPTY,
            ZaimCsvFormat.SETTING_AGGREGATE_EMPTY,
        ]
