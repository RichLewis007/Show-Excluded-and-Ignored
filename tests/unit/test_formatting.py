"""Tests for shared formatting helpers."""

from __future__ import annotations

from rfe.main_window import MainWindow
from rfe.services.formatting import format_bytes, format_match_bytes


def test_format_bytes_handles_none() -> None:
    assert format_bytes(None, empty="n/a") == "n/a"


def test_format_bytes_scales_units() -> None:
    assert format_bytes(0) == "0.00 B"
    assert format_bytes(1024) == "1.00 KB"
    assert format_bytes(1024**2) == "1.00 MB"
    assert format_bytes(1536) == "1.50 KB"


def test_format_bytes_uses_thousand_separators() -> None:
    value = 1024 * 1000  # 1000 KB
    formatted = format_bytes(value)
    number, unit = formatted.split()
    assert number == "1,000.00"
    assert unit == "KB"


def test_format_bytes_supports_integer_precision() -> None:
    assert format_bytes(1024, decimals=0) == "1 KB"


def test_format_match_bytes_handles_thresholds() -> None:
    assert format_match_bytes(0) == "<1 MB"
    assert format_match_bytes(1024**2 - 1) == "<1 MB"
    assert format_match_bytes(1024**2) == "1 MB"


def test_format_elapsed_rounds_seconds() -> None:
    assert MainWindow._format_elapsed(42.2) == "42s"
    assert MainWindow._format_elapsed(75) == "1m 15s"
