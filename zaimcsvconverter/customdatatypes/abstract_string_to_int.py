"""Custom data type to convert string to int."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable

from pydantic import ConfigDict
from pydantic import GetCoreSchemaHandler
from pydantic.v1 import errors

# Reason: Pylint's bug. pylint: disable-next=no-name-in-module
from pydantic.v1.types import ConstrainedNumberMeta
from pydantic.v1.types import OptionalInt
from pydantic.v1.types import int_validator  # type: ignore[attr-defined]
from pydantic.v1.types import strict_int_validator  # type: ignore[attr-defined]
from pydantic.v1.types import update_not_none  # type: ignore[attr-defined]
from pydantic.v1.utils import almost_equal_floats
from pydantic_core.core_schema import no_info_after_validator_function

if TYPE_CHECKING:
    # Reason: Prioritize typing
    from pydantic.v1.types import CallableGenerator  # type: ignore[attr-defined] # noqa: F401
    from pydantic.v1.validators import Number
    from pydantic_core import CoreSchema


class IntegerMustBeFromStr:
    """Validator to convert string to int."""

    def __init__(self, string_to_int: Callable[[str], int]) -> None:
        self.string_to_int = string_to_int

    def validate(self, value: Any) -> int:
        self.raise_if_not_str(value)
        return self.string_to_int(value)

    def raise_if_not_str(self, value: Any) -> None:
        if not isinstance(value, str):
            msg = f"String required. Value is {value}. Type is {type(value)}."
            raise TypeError(msg)


class ConstrainedInt(int, metaclass=ConstrainedNumberMeta):
    """Type that represents a constrained integer."""

    strict: bool = False
    gt: OptionalInt = None
    ge: OptionalInt = None
    lt: OptionalInt = None
    le: OptionalInt = None
    multiple_of: OptionalInt = None

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        return no_info_after_validator_function(cls.validate, handler.generate_schema(str))

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema: dict[str, Any]) -> None:
        update_not_none(
            field_schema,
            exclusiveMinimum=cls.gt,
            exclusiveMaximum=cls.lt,
            minimum=cls.ge,
            maximum=cls.le,
            multipleOf=cls.multiple_of,
        )

    @classmethod
    def validate(cls, value: Any) -> Number:
        value = strict_int_validator(value) if cls.strict else int_validator(value)
        value = cls.number_size_validator(value)
        return cls.number_multiple_validator(value)

    @classmethod
    def number_size_validator(cls, v: Number) -> Number:
        cls.number_size_validator_greater(v)
        cls.number_size_validator_less(v)
        return v

    @classmethod
    def number_size_validator_greater(cls, v: Number) -> None:
        if cls.gt is not None and not v > cls.gt:
            raise errors.NumberNotGtError(limit_value=cls.gt)
        if cls.ge is not None and not v >= cls.ge:
            raise errors.NumberNotGeError(limit_value=cls.ge)

    @classmethod
    def number_size_validator_less(cls, v: Number) -> None:
        if cls.lt is not None and not v < cls.lt:
            raise errors.NumberNotLtError(limit_value=cls.lt)
        if cls.le is not None and not v <= cls.le:
            raise errors.NumberNotLeError(limit_value=cls.le)

    @classmethod
    def number_multiple_validator(cls, v: Number) -> Number:
        if cls.multiple_of is not None:
            mod = float(v) / float(cls.multiple_of) % 1
            if not almost_equal_floats(mod, 0.0) and not almost_equal_floats(mod, 1.0):
                raise errors.NumberNotMultipleError(multiple_of=cls.multiple_of)
        return v


class ConstrainedStringToInt(ConstrainedInt):
    """Type that converts string with comma to int."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def validate(cls, value: Any) -> Number:
        value = cls.integer_must_be_from_str(value)
        return super().validate(value)

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
def constringtoint(  # noqa: PLR0913 pylint: disable=too-many-arguments
    type_name: str,
    type_class: type[ConstrainedStringToInt],
    *,
    strict: bool = False,
    gt: int | None = None,  # pylint: disable=invalid-name
    ge: int | None = None,  # pylint: disable=invalid-name
    lt: int | None = None,  # pylint: disable=invalid-name
    le: int | None = None,  # pylint: disable=invalid-name
    multiple_of: int | None = None,
) -> type[int]:
    """Creates constrained type for converting string with comma to int value."""
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = {"strict": strict, "gt": gt, "ge": ge, "lt": lt, "le": le, "multiple_of": multiple_of}
    return type(type_name, (type_class,), namespace)
