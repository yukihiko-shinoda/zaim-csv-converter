"""Tests for string_with_comma_to_int.py ."""

import datetime
from typing import Any

import pytest
from pydantic.dataclasses import dataclass
from pydantic_core import ValidationError

from pydantictypes.kanji_yen_string_to_int import StrictKanjiYenStringToInt
from tests.pydantictypes import create


@dataclass
class Stub:
    int_: StrictKanjiYenStringToInt


class Test:
    """Tests for StrictKanjiYenStringToInt."""

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("1 円", 1),
            ("1,000 円", 1000),
            ("1,000,000 円", 1000000),
        ],
    )
    def test(self, value: str, expected: int) -> None:
        """Property should be converted to int."""
        stub = create(Stub, [value])
        assert isinstance(stub.int_, int)
        assert stub.int_ == expected

    @pytest.mark.parametrize(
        "value",
        [
            "1.0 円",
            "1.0,000 円",
            "1,000.0 円",
            "1,000,000.0",
            "1,000,000",
            # "1,000,000 円 1,000,000 円",
            # "1,000,000 円 1,000,000",
            # "1,000,000 1,000,000 円",
            "1,000,000 1,000,000",
            # "1000000 円",
            "1000000",
            # "1,000,000円",
            "1 ドル",
            "1ドル",
            "¥1",
            "¥ 1",
            "$1",
            "$ 1",
            "",
            None,
            datetime.date(2020, 1, 1),
            1,
        ],
    )
    def test_error(self, value: Any) -> None:
        """Pydantic should raise ValidationError."""
        with pytest.raises((ValidationError, TypeError)):
            create(Stub, [value])
