"""Custom data type to convert string to datetime."""
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
        return datetime.strptime(value, "%Y/%m/%d")
