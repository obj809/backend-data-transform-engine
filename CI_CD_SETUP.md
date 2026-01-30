# CI/CD Testing Infrastructure

This document describes the complete CI/CD testing infrastructure for the FastAPI backend project.

## Overview

The project includes comprehensive code quality tools, testing with coverage, and automated CI/CD pipelines using GitHub Actions.

## Tools Configured

### 1. Ruff (Linting & Formatting)
- **Purpose**: Fast Python linter and code formatter
- **Configured rules**: pycodestyle, pyflakes, isort, flake8-bugbear, flake8-comprehensions, pyupgrade, flake8-unused-arguments, flake8-simplify
- **Configuration**: `pyproject.toml` under `[tool.ruff]`

### 2. MyPy (Type Checking)
- **Purpose**: Static type checker for Python
- **Features**: Strict type checking with comprehensive warnings
- **Configuration**: `pyproject.toml` under `[tool.mypy]`

### 3. Pytest with Coverage
- **Purpose**: Testing framework with coverage reporting
- **Features**: Unit tests, integration tests, coverage reporting (HTML, XML, terminal)
- **Configuration**: `pyproject.toml` under `[tool.pytest.ini_options]` and `[tool.coverage]`

## Running Quality Checks Locally

### Linting
```bash
# Check for linting issues
ruff check .

# Auto-fix linting issues
ruff check . --fix
```

### Formatting
```bash
# Check formatting (no changes)
ruff format --check .

# Format code
ruff format .
```

### Type Checking
```bash
# Run type checker
mypy .
```

### Testing with Coverage
```bash
# Run tests with coverage report
pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=. --cov-report=html

# Generate XML coverage report (for CI)
pytest --cov=. --cov-report=xml
```

### Run All Checks
```bash
# Run all quality checks in sequence (same as CI)
ruff check . && ruff format --check . && mypy . && pytest --cov=. --cov-report=term-missing
```

## GitHub Actions CI Pipeline

The CI pipeline is configured in `.github/workflows/ci.yml` and runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

### Pipeline Steps

1. **Checkout Code**: Fetch the repository code
2. **Setup Python**: Configure Python environment (versions 3.9, 3.10, 3.11, 3.12)
3. **Install Dependencies**: Install all requirements from `requirements.txt`
4. **Linting**: Run `ruff check .`
5. **Formatting Check**: Run `ruff format --check .`
6. **Type Checking**: Run `mypy .`
7. **Tests with Coverage**: Run `pytest --cov=. --cov-report=xml --cov-report=term-missing`
8. **Upload Coverage**: Upload coverage to Codecov (Python 3.11 only)
9. **Coverage Summary**: Add coverage report to GitHub Actions summary

### Matrix Strategy

The pipeline runs against multiple Python versions:
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

This ensures compatibility across different Python versions.

## Configuration Files

### `pyproject.toml`
Central configuration file containing:
- Ruff linting and formatting rules
- MyPy type checking configuration
- Pytest test discovery settings
- Coverage reporting options

### `requirements.txt`
Dependencies organized into sections:
- **Core dependencies**: FastAPI, Uvicorn, Pydantic, etc.
- **Testing dependencies**: pytest, pytest-cov, httpx
- **Code quality dependencies**: ruff, mypy

### `.gitignore`
Excludes:
- Virtual environments
- Python cache files
- Testing artifacts (.pytest_cache, .coverage, htmlcov/)
- Type checking cache (.mypy_cache)
- Linter cache (.ruff_cache)
- IDE files
- OS-specific files

## Coverage Reports

Coverage reports are generated in three formats:

1. **Terminal**: Displayed in the console with missing line numbers
2. **HTML**: Detailed interactive report in `htmlcov/` directory
3. **XML**: Machine-readable format for CI/CD integration

Current coverage: **100%** for main application code.

## Best Practices

### Before Committing
1. Run `ruff format .` to format your code
2. Run `ruff check .` to lint your code
3. Run `mypy .` to check types
4. Run `pytest` to ensure all tests pass
5. Check coverage with `pytest --cov=.`

### Writing New Code
1. Add type hints to all functions and methods
2. Write tests for new functionality
3. Maintain or improve coverage percentage
4. Follow existing code style and patterns
5. Update documentation as needed

### Pull Requests
1. Ensure all CI checks pass
2. Review coverage changes
3. Add tests for bug fixes
4. Update relevant documentation

## Troubleshooting

### Linting Failures
- Review the specific rule violation
- Use `ruff check . --fix` for auto-fixable issues
- Check `pyproject.toml` for rule configuration

### Type Checking Failures
- Add missing type hints
- Check for incompatible types
- Review MyPy documentation for specific errors
- Use `# type: ignore` sparingly with comments explaining why

### Test Failures
- Run tests locally with `pytest -v` for verbose output
- Check test isolation issues
- Verify test data and fixtures
- Review error messages and tracebacks

### Coverage Drops
- Add tests for uncovered code paths
- Check for unreachable code
- Review coverage report: `pytest --cov=. --cov-report=html`
- Open `htmlcov/index.html` in browser for detailed view

## Continuous Improvement

- Regularly update dependencies
- Add more comprehensive tests
- Increase coverage targets
- Add integration tests
- Configure additional code quality tools as needed
- Monitor CI/CD performance and optimize

## Resources

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
