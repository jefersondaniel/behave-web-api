# Agent Guidelines

## Commit Convention
- Use [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages.
- Examples:
  - `fix: update bottle dependency`
  - `docs: add contribution guide`

## Testing
- Install dependencies: `uv pip install --system -e ".[test]"`
- Run the full test suite: `./runtests.sh`

## Coverage
- Generate coverage:
  - `coverage erase`
  - `pytest --cov=behave_web_api --cov-report=term-missing`
  - `BASE_URL=localhost:5000 coverage run --append -m behave features/requests.feature`
  - `coverage report -m`
- Ensure coverage does not decrease.

## Python Version
- Use Python 3.11 or newer.
