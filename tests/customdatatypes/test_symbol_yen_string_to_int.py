"""Tests for symbol_yen_string_to_int.py ."""

import datetime
from typing import Any

from pydantic.dataclasses import dataclass
from pydantic import ValidationError
import pytest

from tests.customdatatypes import create
from zaimcsvconverter.customdatatypes.symbol_yen_string_to_int import SymbolYenStringToInt


@dataclass
class Stub:
    int_: SymbolYenStringToInt


class Test:
    """Tests for SymbolYenStringToInt."""

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (r"\1", 1),
            (r"\1,000", 1000),
            (r"\1,000,000", 1000000),
        ],
    )
    def test(self, value: str, expected: int) -> None:
        """Property should be converted to int."""
        stub = create(Stub, [value])
        assert stub.int_ == expected
        assert isinstance(stub.int_, int)

    @pytest.mark.parametrize(
        "value",
        [
            r"\1.0",
            r"\1,000.0",
            r"\1,000,000.0",
            # r"\1,000,000 \1,000,000",
            # r"\1000000",
            # r"\1,000,000円",
            # r"\1 円",
            # r"\1円",
            # r"\1 ドル",
            # r"\1ドル",
            r"¥1",
            r"¥ 1",
            r"$1",
            r"$ 1",
            "",
            None,
            datetime.date(2020, 1, 1),
            1,
        ],
    )
    def test_error(self, value: Any) -> None:
        """Property should be converted to int."""
        with pytest.raises(ValidationError):
            create(Stub, [value])
