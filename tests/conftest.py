"""Shared pytest configuration."""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    root = Path(__file__).resolve().parents[1]
    src_dir = root / "src"
    src_str = str(src_dir)
    if src_dir.exists() and src_str not in sys.path:
        sys.path.insert(0, src_str)


_ensure_src_on_path()
