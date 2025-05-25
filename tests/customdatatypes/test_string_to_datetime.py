"""Tests for string_to_datetime.py ."""

import datetime
from typing import Any

import pytest
from pydantic import ValidationError
from pydantic.dataclasses import dataclass

from tests.customdatatypes import create
from zaimcsvconverter.customdatatypes.string_to_datetime import (
    StringNumberOnlyToDateTime,
    StringSlashMonthDayOnlyToDatetime,
    StringSlashToDateTime,
)


@dataclass
class StubStringSlashToDateTime:
    date_: StringSlashToDateTime


class TestStringSlashToDateTime:
    """Tests for StringSlashToDateTime."""

    @pytest.mark.parametrize(
        ("value", "expected_year", "expected_month", "expected_day"),
        [
            ("2020/01/01", 2020, 1, 1),
            ("2020/01/1", 2020, 1, 1),
            ("2020/1/01", 2020, 1, 1),
            ("2020/12/31", 2020, 12, 31),
            ("2020/02/29", 2020, 2, 29),
        ],
    )
    def test(self, value: str, expected_year: int, expected_month: int, expected_day: int) -> None:
        """Property should be converted to datetime.date."""
        stub = create(StubStringSlashToDateTime, [value])
        assert isinstance(stub.date_, datetime.date)
        assert stub.date_.year == expected_year
        assert stub.date_.month == expected_month
        assert stub.date_.day == expected_day

    @pytest.mark.parametrize(
        "value",
        [
            "2020/01/00",
            "2020/01/32",
            "2020/00/01",
            "2020/13/01",
            "2020/02/30",
            "2020-01-01",
            "20200101",
            "2020/01/01/01",
            "2020/01",
            "2020",
            "",
            None,
            datetime.date(2020, 1, 1),
            1,
        ],
    )
    def test_error(self, value: Any) -> None:
        """Pydantic should raise ValidationError."""
        with pytest.raises(ValidationError):
            create(StubStringSlashToDateTime, [value])


@dataclass
class StubStringNumberOnlyToDateTime:
    date_: StringNumberOnlyToDateTime


class TestStringNumberOnlyToDateTime:
    """Tests for StringNumberOnlyToDateTime."""

    @pytest.mark.parametrize(
        ("value", "expected_year", "expected_month", "expected_day"),
        [
            ("20200101", 2020, 1, 1),
            ("20201231", 2020, 12, 31),
            ("20200229", 2020, 2, 29),
        ],
    )
    def test(self, value: str, expected_year: int, expected_month: int, expected_day: int) -> None:
        """Property should be converted to datetime.date."""
        stub = create(StubStringNumberOnlyToDateTime, [value])
        assert isinstance(stub.date_, datetime.date)
        assert stub.date_.year == expected_year
        assert stub.date_.month == expected_month
        assert stub.date_.day == expected_day

    @pytest.mark.parametrize(
        "value",
        [
            "20200100",
            "20200132",
            "20200001",
            "20201301",
            "20200230",
            "2020-01-01",
            "2020/01/01",
            "2020010101",
            "2020011",
            "2020101",
            "202001",
            "2020",
            "",
            None,
            datetime.date(2020, 1, 1),
            1,
        ],
    )
    def test_error(self, value: Any) -> None:
        """Pydantic should raise ValidationError."""
        with pytest.raises(ValidationError):
            create(StubStringNumberOnlyToDateTime, [value])


@dataclass
class StubStringSlashMonthDayOnlyToDatetime:
    date_: StringSlashMonthDayOnlyToDatetime


class TestStringSlashMonthDayOnlyToDatetime:
    """Tests for StringSlashMonthDayOnlyToDatetime."""

    @pytest.mark.parametrize(
        ("value", "expected_month", "expected_day"),
        [
            ("01/01", 1, 1),
            ("12/31", 12, 31),
            ("02/29", 2, 29),
        ],
    )
    def test(self, value: str, expected_month: int, expected_day: int) -> None:
        """Property should be converted to datetime.date."""
        expected_year = 1904
        stub = create(StubStringSlashMonthDayOnlyToDatetime, [value])
        assert isinstance(stub.date_, datetime.date)
        assert stub.date_.year == expected_year
        assert stub.date_.month == expected_month
        assert stub.date_.day == expected_day

    @pytest.mark.parametrize(
        "value",
        [
            "01/00",
            "01/32",
            "00/01",
            "13/01",
            "02/30",
            "01-01",
            "0101",
            "2020/01/01",
            "01/01/01",
            "01/1",
            "1/01",
            "/01",
            "01/",
            "01",
            "",
            None,
            datetime.date(2020, 1, 1),
            1,
        ],
    )
    def test_error(self, value: Any) -> None:
        """Pydantic should raise ValidationError."""
        with pytest.raises(ValidationError):
            create(StubStringNumberOnlyToDateTime, [value])
