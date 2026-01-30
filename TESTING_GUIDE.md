# Testing Guide

## Quick Start

### Install Development Dependencies
```bash
pip install -r requirements.txt
```

## Running All Quality Checks

### Complete Check (Same as CI)
```bash
ruff check . && ruff format --check . && mypy . && pytest --cov=. --cov-report=term-missing
```

### Individual Checks

#### 1. Linting with Ruff
```bash
# Check for issues
ruff check .

# Auto-fix issues
ruff check . --fix

# Check specific file
ruff check main.py
```

#### 2. Code Formatting with Ruff
```bash
# Check formatting (no changes)
ruff format --check .

# Format code
ruff format .

# Format specific file
ruff format main.py
```

#### 3. Type Checking with MyPy
```bash
# Check all files
mypy .

# Check specific file
mypy main.py

# Verbose output
mypy . --verbose
```

#### 4. Run Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py

# Run specific test
pytest tests/test_main.py::test_health_check
```

#### 5. Test Coverage
```bash
# Run with terminal coverage report
pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report (opens in browser)
pytest --cov=. --cov-report=html
open htmlcov/index.html

# Generate XML coverage (for CI)
pytest --cov=. --cov-report=xml
```

## Pre-Commit Checklist

Before committing code, ensure:
- [ ] Code is formatted: `ruff format .`
- [ ] No linting errors: `ruff check .`
- [ ] Type checking passes: `mypy .`
- [ ] All tests pass: `pytest`
- [ ] Coverage maintained: `pytest --cov=.`

## Writing Tests

### Test Structure
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_endpoint_name() -> None:
    # Arrange
    expected_response = {"key": "value"}

    # Act
    response = client.get("/endpoint")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_response
```

### Test Markers
```python
import pytest

@pytest.mark.unit
def test_unit_function() -> None:
    pass

@pytest.mark.integration
def test_integration_endpoint() -> None:
    pass
```

Run specific markers:
```bash
pytest -m unit
pytest -m integration
```

## Coverage Goals

- **Minimum**: 80% coverage
- **Target**: 90% coverage
- **Current**: 100% coverage

### View Missing Coverage
```bash
pytest --cov=. --cov-report=term-missing
```

### Generate HTML Report
```bash
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs:

1. Linting check
2. Formatting check
3. Type checking
4. Tests with coverage
5. Coverage upload to Codecov

All checks must pass for the pipeline to succeed.

## Troubleshooting

### Common Issues

#### Linting Failures
```bash
# View specific errors
ruff check .

# Auto-fix where possible
ruff check . --fix
```

#### Type Errors
```bash
# Detailed output
mypy . --verbose

# Show error codes
mypy . --show-error-codes
```

#### Test Failures
```bash
# Verbose test output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x
```

#### Import Errors
```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

## Best Practices

### Type Hints
Always add type hints to functions:
```python
def process_data(input: str) -> dict[str, str]:
    return {"result": input}
```

### Test Naming
- Use descriptive test names: `test_endpoint_returns_correct_status`
- Follow pattern: `test_<what>_<condition>_<expected_result>`

### Coverage
- Test happy paths and edge cases
- Test error handling
- Test validation logic

### Code Organization
- Keep functions small and focused
- Separate business logic from HTTP handling
- Use dependency injection for testability
