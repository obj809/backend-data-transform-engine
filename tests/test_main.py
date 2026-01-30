import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from middleware import DEFAULT_CORS_ORIGINS, get_cors_origins

client = TestClient(app)


def test_read_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


class TestGetCorsOrigins:
    def test_default_origins_when_env_not_set(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            origins = get_cors_origins()
            assert origins == DEFAULT_CORS_ORIGINS
            assert origins is not DEFAULT_CORS_ORIGINS

    def test_default_origins_when_env_empty(self) -> None:
        with patch.dict(os.environ, {"CORS_ORIGINS": ""}, clear=True):
            origins = get_cors_origins()
            assert origins == DEFAULT_CORS_ORIGINS

    def test_default_origins_when_env_whitespace(self) -> None:
        with patch.dict(os.environ, {"CORS_ORIGINS": "   "}, clear=True):
            origins = get_cors_origins()
            assert origins == DEFAULT_CORS_ORIGINS

    def test_parse_single_origin(self) -> None:
        with patch.dict(os.environ, {"CORS_ORIGINS": "http://example.com"}, clear=True):
            origins = get_cors_origins()
            assert origins == ["http://example.com"]

    def test_parse_comma_separated_origins(self) -> None:
        with patch.dict(
            os.environ,
            {"CORS_ORIGINS": "http://example.com,http://localhost:3000"},
            clear=True,
        ):
            origins = get_cors_origins()
            assert origins == ["http://example.com", "http://localhost:3000"]

    def test_strips_whitespace_around_origins(self) -> None:
        with patch.dict(
            os.environ,
            {"CORS_ORIGINS": "  http://example.com  ,  http://localhost:3000  "},
            clear=True,
        ):
            origins = get_cors_origins()
            assert origins == ["http://example.com", "http://localhost:3000"]

    def test_filters_empty_entries(self) -> None:
        with patch.dict(
            os.environ,
            {"CORS_ORIGINS": "http://example.com,,http://localhost:3000,"},
            clear=True,
        ):
            origins = get_cors_origins()
            assert origins == ["http://example.com", "http://localhost:3000"]
