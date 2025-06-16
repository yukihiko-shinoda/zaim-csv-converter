"""Custom data type to convert yen string to int."""

from __future__ import annotations

from typing import Annotated

import annotated_types
from pydantic import BeforeValidator

# Reason: Pylint's bug. pylint: disable=no-name-in-module
from pydantictypes.abstract_string_to_int import IntegerMustBeFromStr
from zaimcsvconverter.utility import Utility


# Reason: Followed Pydantic specification.
def constringtoint(  # noqa: PLR0913  # pylint: disable=too-many-arguments
    *,
    strict: bool | None = None,  # noqa: ARG001  # pylint: disable=unused-argument
    gt: int | None = None,
    ge: int | None = None,
    lt: int | None = None,
    le: int | None = None,
    multiple_of: int | None = None,
) -> type[int]:
    """A wrapper around `int` that allows for additional constraints.

    Args:
        strict: Whether to validate the integer in strict mode. Defaults to `None`.
        gt: The value must be greater than this.
        ge: The value must be greater than or equal to this.
        lt: The value must be less than this.
        le: The value must be less than or equal to this.
        multiple_of: The value must be a multiple of this.

    Returns:
        The wrapped integer type.
    """
    return Annotated[  # type: ignore[return-value]
        int,
        BeforeValidator(IntegerMustBeFromStr(Utility.convert_kanji_yen_string_to_int).validate),
        annotated_types.Interval(gt=gt, ge=ge, lt=lt, le=le),
        annotated_types.MultipleOf(multiple_of) if multiple_of is not None else None,
    ]


StrictKanjiYenStringToInt = Annotated[
    int,
    BeforeValidator(IntegerMustBeFromStr(Utility.convert_kanji_yen_string_to_int).validate),
]
