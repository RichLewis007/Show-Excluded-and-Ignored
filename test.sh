#!/usr/bin/env bash

  uv run --extra dev pytest

#   - **Run the entire suite:**
#   ```bash
#   uv run --extra dev pytest
#   ```

# - **Run a single test module (e.g. the new integration test):**
#   ```bash
#   uv run --extra dev pytest tests/integration/test_scanner_finds_excluded_patterns.py
#   ```

# - **Run one specific test function if you want to zoom in further:**
#   ```bash
#   uv run --extra dev pytest tests/integration/test_scanner_finds_excluded_patterns.py::test_match_engine_flags_patterns
#   ```

# Each command uses the dev extras so pytest and plugins are available.

# uv run --extra dev pytest tests/integration/test_scanner_finds_excluded_patterns.py::fixture_patterns_dir(./tmp)
#  fixture_patterns_dir(tmp_path: Pa
