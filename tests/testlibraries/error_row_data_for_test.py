"""This module implements data class for wrapping list of error CSV row model."""

from dataclasses import dataclass


@dataclass
class ErrorRowDataForTest:
    """This class implements data class for wrapping list of error CSV row model."""

    convert_table: str
    store_name: str
    item_name: str
