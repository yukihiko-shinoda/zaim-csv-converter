"""Custom data types."""
from decimal import Decimal
from typing import Any, Optional, TYPE_CHECKING, Union

# Reason: Pylint's bug.
from pydantic import ConstrainedInt  # pylint: disable=no-name-in-module

from zaimcsvconverter.customdatatypes.validators import (
    optional_int_validator,
    optional_number_multiple_validator,
    optional_number_size_validator,
    optional_strict_int_validator,
    string_validator,
)

Number = Union[int, float, Decimal]


if TYPE_CHECKING:
    # Reason: Prioritize typing
    from pydantic.types import CallableGenerator  # type: ignore[attr-defined]


class StringToOptionalInt(ConstrainedInt):
    """Optional pydantic ConstrainedInt from str."""

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield string_validator
        yield cls.convert_to_optional_integer
        yield optional_strict_int_validator if cls.strict else optional_int_validator
        yield optional_number_size_validator
        yield optional_number_multiple_validator

    @classmethod
    def convert_to_optional_integer(cls, value: Any) -> Optional[int]:
        """Optional integer must be from str."""
        if not value:
            return None
        return int(value)


# Reason: To follow pydantic constr interface.
def constringtooptionalint(  # noqa: PLR0913 pylint: disable=too-many-arguments
    *,
    strict: bool = False,
    gt: Optional[int] = None,  # pylint: disable=invalid-name
    ge: Optional[int] = None,  # pylint: disable=invalid-name
    lt: Optional[int] = None,  # pylint: disable=invalid-name
    le: Optional[int] = None,  # pylint: disable=invalid-name
    multiple_of: Optional[int] = None,
) -> type[int]:
    """Optional pydantic conint from str."""
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = {"strict": strict, "gt": gt, "ge": ge, "lt": lt, "le": le, "multiple_of": multiple_of}
    return type("ConstrainedStringToOptionalIntValue", (StringToOptionalInt,), namespace)


if TYPE_CHECKING:
    ConstrainedStringToOptionalInt = Optional[int]
else:
    ConstrainedStringToOptionalInt = constringtooptionalint()
