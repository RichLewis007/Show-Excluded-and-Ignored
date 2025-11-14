"""Tests for accumulating match sizes in the scan worker."""

from __future__ import annotations

import time
from collections.abc import Generator
from itertools import pairwise
from pathlib import Path
from threading import Thread

import pytest
from PySide6.QtCore import QCoreApplication

from rfe.models.rules_model import Rule
from rfe.workers.scan_worker import ScanPayload, ScanWorker


@pytest.fixture(scope="session", autouse=True)
def _qt_core_app() -> Generator[QCoreApplication, None, None]:
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    yield app


def _write_file(path: Path, size: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\0" * size)


def test_scan_worker_accumulates_matched_bytes(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()

    excluded_dir = root / "excluded"
    nested_dir = excluded_dir / "nested"
    nested_dir.mkdir(parents=True)

    _write_file(excluded_dir / "first.bin", 10)
    _write_file(nested_dir / "second.bin", 20)
    _write_file(root / "kept.bin", 50)

    rules = [
        Rule(action="-", pattern="excluded/**", lineno=1),
        Rule(action="-", pattern="excluded/nested/second.bin", lineno=2),
    ]

    worker = ScanWorker(root_path=root, rules=rules)
    emissions: list[tuple[int, int, int, int, float, str]] = []
    worker.progress.connect(lambda *args: emissions.append(args))

    payload = worker._run_scan()
    assert isinstance(payload, ScanPayload)

    expected_bytes = 30
    assert payload.stats.matched_bytes == expected_bytes
    assert emissions, "expected at least one progress emission"

    bytes_progress = [entry[3] for entry in emissions]
    assert bytes_progress[-1] == expected_bytes
    assert all(a <= b for a, b in pairwise(bytes_progress))
    assert emissions[-1][5] == "done"


def test_scan_worker_pause_and_resume(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()

    excluded_dir = root / "pausedir"
    excluded_dir.mkdir()
    _write_file(excluded_dir / "file1.bin", 5)

    rules = [Rule(action="-", pattern="pausedir/**", lineno=1)]

    worker = ScanWorker(root_path=root, rules=rules)
    results: list[ScanPayload | None] = []

    def run_scan() -> None:
        results.append(worker._run_scan())

    worker.request_pause()
    thread = Thread(target=run_scan, daemon=True)
    thread.start()

    time.sleep(0.1)
    assert thread.is_alive(), "worker should block while paused"

    worker.request_resume()
    thread.join(timeout=2)
    assert not thread.is_alive(), "worker should finish after resume"
    assert results and isinstance(results[0], ScanPayload)
