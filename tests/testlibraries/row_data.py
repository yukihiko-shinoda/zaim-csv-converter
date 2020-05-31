"""This module implements data class for wrapping list of CSV row model."""
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class ZaimRowData:
    """This class implements data class for wrapping list of Zaim CSV row model."""

    # Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
    date: Optional[Union[str, int]]
    method: Optional[Union[str, int]]
    category_large: Optional[Union[str, int]]
    category_small: Optional[Union[str, int]]
    cash_flow_source: Optional[Union[str, int]]
    cash_flow_target: Optional[Union[str, int]]
    item_name: Optional[Union[str, int]]
    note: Optional[Union[str, int]]
    store_name: Optional[Union[str, int]]
    currency: Optional[Union[str, int]]
    amount_income: Optional[Union[str, int]]
    amount_payment: Optional[Union[str, int]]
    amount_transfer: Optional[Union[str, int]]
    balance_adjustment: Optional[Union[str, int]]
    amount_before_currency_conversion: Optional[Union[str, int]]
    setting_aggregate: Optional[Union[str, int]]


@dataclass
class InvalidRowErrorRowData:
    """This class implements data class for wrapping list of invalid row error CSV row model."""

    input_file_name: str
    index: str
    error: str
