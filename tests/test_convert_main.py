# Copyright (c) 2018 Yukihiko Shinoda
"""Tests for convert.py entry point without config file."""

from __future__ import annotations

import pytest

import convert
from zaimcsvconverter.zaim_csv_converter import ZaimCsvConverter


def test_main_reports_missing_config_and_exits_2(monkeypatch: pytest.MonkeyPatch, tmp_path, capsys) -> None:
    """Missing config.yml should be a clean error, not a raw traceback."""
    monkeypatch.setattr(convert, "PATH_FILE_CONFIG", tmp_path / "config.yml")
    with pytest.raises(SystemExit) as exited:
        convert.main()
    assert exited.value.code == 2
    assert "config.yml.dist" in capsys.readouterr().err


def test_execute_mentions_dist_when_config_missing(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Library entry should point at config.yml.dist when config is absent."""
    from zaimcsvconverter import zaim_csv_converter

    monkeypatch.setattr(zaim_csv_converter, "PATH_FILE_CONFIG", tmp_path / "config.yml")
    with pytest.raises(FileNotFoundError, match="config.yml.dist"):
        ZaimCsvConverter.execute()
