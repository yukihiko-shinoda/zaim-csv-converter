"""Custom data type to convert string to datetime."""
from abc import abstractmethod
from datetime import datetime
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    # Reason: Prioritize typing
    from pydantic.types import CallableGenerator  # type: ignore[attr-defined]


class StringToDateTime(datetime):
    """Type that converts string to datetime."""

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.datetime_must_be_from_str
        yield cls.parse_date

    @classmethod
    def datetime_must_be_from_str(cls, value: Any) -> str:
        if not isinstance(value, str):
            msg = "string required"
            raise TypeError(msg)
        return value

    @classmethod
    def parse_date(cls, value: Any) -> datetime:
        # Reason: Time is not used in this process.
        return datetime.strptime(value, cls.get_format())  # noqa: DTZ007

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
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.datetime_must_be_from_str
        yield cls.eight_digits_required
        yield cls.parse_date

    @classmethod
    def eight_digits_required(cls, value: str) -> str:
        number_digit = 8
        if len(value) != number_digit:
            msg = "8 digits required"
            raise ValueError(msg)
        return value

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
            msg = "string required"
            raise TypeError(msg)
        # Reason: Time is not used in this process.
        return datetime.strptime(f"1904/{value}", "%Y/%m/%d")  # noqa: DTZ007
