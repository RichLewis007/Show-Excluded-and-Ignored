#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

uv run --extra dev pyinstaller --clean --noconfirm ghost_files_finder.spec

echo "PyInstaller build complete. Dist output is located in $(realpath dist)."
