# Agent Guidelines

## Commit Convention
- Use [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages.
- Examples:
  - `fix: update bottle dependency`
  - `docs: add contribution guide`

## Dependencies
- Use `uv add` to add runtime dependencies.
- Use `uv add --group test` for dev/test dependencies.

## Testing
- Sync dependencies: `uv sync --all-extras`
- Run the full test suite: `uv run ./runtests.sh`

## Coverage
- Generate coverage:
  - `uv run coverage erase`
  - `uv run pytest --cov=behave_web_api --cov-report=term-missing`
  - `BASE_URL=localhost:5000 uv run coverage run --append -m behave features/requests.feature`
  - `uv run coverage report -m`
- Ensure coverage does not decrease.

## Python Version
- Use Python 3.11 or newer.
