"""Custom data type to convert string with comma to int."""
from abc import abstractmethod
from typing import Any, Optional, TYPE_CHECKING

# Reason: Pylint's bug. pylint: disable=no-name-in-module
from pydantic import ConstrainedInt

if TYPE_CHECKING:
    # Reason: Prioritize typing
    from pydantic.types import CallableGenerator  # type: ignore[attr-defined]


class ConstrainedStringToInt(ConstrainedInt):
    """Type that converts string with comma to int."""

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.integer_must_be_from_str
        yield from super().__get_validators__()

    @classmethod
    def integer_must_be_from_str(cls, value: Any) -> int:
        if not isinstance(value, str):
            msg = "string required"
            raise TypeError(msg)
        return cls.string_to_int(value)

    @classmethod
    @abstractmethod
    def string_to_int(cls, value: str) -> int:
        raise NotImplementedError


# Reason: Followed pydantic specification.
def constringtoint(  # noqa: PLR0913
    type_name: str,
    type_class: type[ConstrainedStringToInt],
    *,
    strict: bool = False,
    gt: Optional[int] = None,  # pylint: disable=invalid-name
    ge: Optional[int] = None,  # pylint: disable=invalid-name
    lt: Optional[int] = None,  # pylint: disable=invalid-name
    le: Optional[int] = None,  # pylint: disable=invalid-name
    multiple_of: Optional[int] = None,
) -> type[int]:
    """Creates constrained type for converting string with comma to int value."""
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = {"strict": strict, "gt": gt, "ge": ge, "lt": lt, "le": le, "multiple_of": multiple_of}
    return type(type_name, (type_class,), namespace)
