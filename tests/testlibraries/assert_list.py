"""To reduce cyclomatic complexity."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from collections.abc import Iterable


def assert_each_properties(
    actual_object: object,
    list_expected: list[Any],
    *,
    attribute_filter: list[str] | None = None,
) -> None:
    """Asserts each properties of actual object."""
    list_actual = create_actual_iterator(actual_object, attribute_filter)
    try:
        assert_list(list_actual, list_expected)
    except AssertionError as error:
        raise AssertionError(str(actual_object.__dict__.keys()) + ",\n" + str(error)) from error


def create_actual_iterator(actual_object: object, attribute_filter: list[str] | None = None) -> Iterable[Any]:
    return (
        value
        for key, value in actual_object.__dict__.items()
        if not key.startswith("_") and (attribute_filter is None or key in attribute_filter)
    )


def assert_list(iterable_actual: Iterable[Any], list_expected: list[Any]) -> None:
    index = 0
    for actual in iterable_actual:
        assert actual == list_expected[index], f"index: {index}, actual: {actual}, expected: {list_expected[index]}"
        index += 1
    assert index == len(list_expected), f"index: {index}, expected: {len(list_expected)}"
