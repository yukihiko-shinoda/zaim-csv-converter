"""This module implements data class for wrapping list of CSV row model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ZaimRowData:
    """This class implements data class for wrapping list of Zaim CSV row model."""

    # Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
    date: str | int | None
    method: str | int | None
    category_large: str | int | None
    category_small: str | int | None
    cash_flow_source: str | int | None
    cash_flow_target: str | int | None
    item_name: str | int | None
    note: str | int | None
    store_name: str | int | None
    currency: str | int | None
    amount_income: str | int | None
    amount_payment: str | int | None
    amount_transfer: str | int | None
    balance_adjustment: str | int | None
    amount_before_currency_conversion: str | int | None
    setting_aggregate: str | int | None


@dataclass
class InvalidRowErrorRowData:
    """This class implements data class for wrapping list of invalid row error CSV row model."""

    input_file_name: str
    index: str
    error: str
