from __future__ import annotations

# -------------------------------------------------------------
# create-samples.py
#
# Utility script that builds a sample directory tree containing
# one example for every pattern defined in an rclone filter list file.
# This is the same data our integration test fabricates; it can
# be used for manual QA, GUI demos, or to inspect which files are
# considered “excluded”.
#
# Usage:
#
#   uv run --extra dev python create-samples.py
#
# Optional flags:
#
#   --output PATH   Destination directory (default: ./tmp-sample)
#   --force         Overwrite the destination if it already exists
#
# Example:
#
#   uv run --extra dev python create-samples.py --output ./temp/samples --force
#
# Note: In uv, --extra dev tells it to resolve the optional dependency group
# named dev from your pyproject.toml while executing the command. That way
# tools like pytest, mypy, or pre-commit (listed under [project.optional-dependencies].dev)
# are available for the run. Without the flag, uv would only install the core project dependencies.
#
# -------------------------------------------------------------
import argparse
import shutil
from pathlib import Path
from typing import Protocol, cast

from tests.integration.test_scanner_finds_excluded_patterns import fixture_patterns_dir


def create_samples(destination: Path, *, force: bool) -> Path:
    """Create the sample tree at ``destination``.

    Args:
        destination: Directory where the structure should be created.
        force: If True, overwrite the destination when it already exists.

    Returns:
        The destination path.
    """
    if destination.exists():
        if not force:
            raise FileExistsError(
                f"Destination {destination} already exists. Use --force to overwrite."
            )
        shutil.rmtree(destination)

    destination.mkdir(parents=True, exist_ok=True)

    class _PatternsDirFactory(Protocol):
        def __call__(self, *, tmp_path: Path) -> Path: ...

    factory = cast(_PatternsDirFactory, getattr(fixture_patterns_dir, "__wrapped__", None))
    if factory is None:
        raise RuntimeError("fixtures_patterns_dir.__wrapped__ is unavailable.")
    factory(tmp_path=destination)

    # The integration fixture builds its structure at ``tmp_path / "samples"``.
    # When users pass an explicit destination (e.g., ./temp/samples) we only
    # want that single directory, so flatten any nested ``samples`` folder.
    nested = destination / "samples"
    if nested.exists() and nested.is_dir():
        for child in list(nested.iterdir()):
            target = destination / child.name
            if target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            child.rename(target)
        shutil.rmtree(nested)

    return destination


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Create a sample directory tree containing every pattern from a given rclone filter list file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("./temp"),
        help="Destination directory for generated samples (default: %(default)s).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the destination directory if it already exists.",
    )

    args = parser.parse_args()
    target = create_samples(args.output, force=args.force)
    print(f"Created sample tree at {target.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
