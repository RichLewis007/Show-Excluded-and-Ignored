# Show Excluded and Ignored

Desktop app for exploring files that match rclone filter rules. Built with PySide6 and managed with `uv`.

## Development

1. Install uv: <https://github.com/astral-sh/uv>
2. Sync dependencies:
   ```
   uv sync
   ```
3. Enable git hooks:
   ```
   uv run pre-commit install
   ```
4. Run quality checks:
   ```
   uv run nox
   ```
5. Launch the app in dev mode:
   ```
   uv run show-excluded-and-ignored
   ```

## Status

Early scaffolding stage. Refer to `docs/program-specifications.md` for the roadmap.

