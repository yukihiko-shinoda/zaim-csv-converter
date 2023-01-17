"""Custom data type to convert string to datetime."""
from abc import abstractmethod
from datetime import datetime
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    # Reason: Prioritize typing
    from pydantic.types import CallableGenerator  # type: ignore


class StringToDateTime(datetime):
    """Type that converts string to datetime."""

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.parse_date

    @classmethod
    def parse_date(cls, value: Any) -> datetime:
        if not isinstance(value, str):
            raise TypeError("string required")
        return datetime.strptime(value, cls.get_format())

    @classmethod
    @abstractmethod
    def get_format(cls) -> str:
        raise NotImplementedError


class StringSlashToDateTime(StringToDateTime):
    """Type that converts string to datetime."""

    @classmethod
    def get_format(cls) -> str:
        return "%Y/%m/%d"


class StringNumberOnlyToDateTime(StringToDateTime):
    """Type that converts string to datetime."""

    @classmethod
    def get_format(cls) -> str:
        return "%Y%m%d"


class StringSlashMonthDayOnlyToDatetime(datetime):
    """Type that converts string to datetime."""

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.parse_date

    @classmethod
    def parse_date(cls, value: Any) -> datetime:
        if not isinstance(value, str):
            raise TypeError("string required")
        return datetime.strptime(f"1904/{value}", "%Y/%m/%d")
