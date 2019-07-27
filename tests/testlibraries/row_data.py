"""This module implements data class for wrapping list of CSV row model."""
from dataclasses import dataclass


@dataclass
class ZaimRowData:
    """This class implements data class for wrapping list of Zaim CSV row model."""
    date: str
    method: str
    category_large: str
    category_small: str
    cash_flow_source: str
    cash_flow_target: str
    item_name: str
    note: str
    store_name: str
    currency: str
    amount_income: str
    amount_payment: str
    amount_transfer: str
    balance_adjustment: str
    amount_before_currency_conversion: str
    setting_aggregate: str


@dataclass
class InvalidRowErrorRowData:
    """This class implements data class for wrapping list of invalid row error CSV row model."""
    input_file_name: str
    index: str
    error: str
