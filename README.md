# Backend Data Transform Engine

![CI](https://github.com/obj809/backend-data-transform-engine/actions/workflows/ci.yml/badge.svg)

FastAPI backend service for data transformation.

## Quick Start

```bash
# Local
uvicorn main:app --reload

# Docker (development)
docker-compose --profile dev up api-dev

# Docker (production)
docker build -t data-transform-api .
docker run -p 8000:8000 data-transform-api
```

## API

| Endpoint  | Description  |
|-----------|--------------|
| `/`       | Hello World  |
| `/health` | Health check |

Docs: http://localhost:8000/docs

## Testing

```bash
pytest -v                                      # Local
docker-compose --profile test run --rm test    # Docker
```

## Environment Variables

| Variable       | Description                | Default                                          |
|----------------|----------------------------|--------------------------------------------------|
| `CORS_ORIGINS` | Allowed origins (CSV)      | `http://localhost:3000,http://172.20.10.2:3000` |

## Project Structure

```
├── main.py           # App entry point
├── middleware.py     # CORS configuration
├── Dockerfile        # Production image
├── Dockerfile.dev    # Development image
└── tests/            # Unit tests
```
