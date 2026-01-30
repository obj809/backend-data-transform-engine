# FastAPI Commands


## Running the Server

Development mode with auto-reload:

```bash
uvicorn main:app --reload
```

Specify host and port:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```


## Virtual Environment Setup

```bash
# Create venv
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

## Installation

```bash
pip install fastapi uvicorn

# Save dependencies
pip freeze > requirements.txt
```

## Accessing the API

- **API Root**: http://localhost:8000
- **Swagger UI Docs**: http://localhost:8000/docs
- **ReDoc Docs**: http://localhost:8000/redoc

## Testing Endpoints

```bash
# GET request
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_main.py

# Run a specific test
pytest tests/test_main.py::test_health_check

# Run tests with coverage
pytest --cov=. --cov-report=html --cov-report=term-missing

# Run tests with coverage (XML format for CI)
pytest --cov=. --cov-report=xml --cov-report=term-missing
```

## Code Quality and Linting

### Linting with Ruff

```bash
# Run linting checks
ruff check .

# Run linting with auto-fix
ruff check . --fix

# Run linting on a specific file
ruff check main.py
```

### Formatting with Ruff

```bash
# Check formatting (without making changes)
ruff format --check .

# Format all files
ruff format .

# Format a specific file
ruff format main.py
```

### Type Checking with MyPy

```bash
# Run type checking on all files
mypy .

# Run type checking on a specific file
mypy main.py

# Run type checking with verbose output
mypy . --verbose
```

### Run All Quality Checks

```bash
# Run all quality checks in sequence
ruff check . && ruff format --check . && mypy . && pytest --cov=. --cov-report=term-missing
```

## Git Hooks

Install the pre-push hook to run tests automatically before each push:

```bash
cp scripts/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```
