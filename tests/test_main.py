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


class TestUploadFile:
    def test_upload_valid_stock_data(self) -> None:
        file_content = b"""[
            {
                "symbol": "^AXJO",
                "name": "S&P/ASX 200",
                "price": 8929.41,
                "change": 7.53,
                "change_percent": 0.084399,
                "day_high": 8948.55,
                "day_low": 8903.81,
                "previous_close": 8921.88,
                "timestamp": "2026-01-28T12:42:18"
            },
            {
                "symbol": "^AXJO",
                "name": "S&P/ASX 200",
                "price": 8971.71,
                "change": 12.24,
                "change_percent": 0.136615,
                "day_high": 8996.19,
                "day_low": 8949.59,
                "previous_close": 8959.47,
                "timestamp": "2026-01-28T12:43:18"
            }
        ]"""
        response = client.post(
            "/upload",
            files={"file": ("test.json", file_content, "application/json")},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "^AXJO"
        assert data["name"] == "S&P/ASX 200"
        assert data["price"] == 8950.56
        assert data["timestamp"] == "(current UTC time)"

    def test_upload_invalid_file_type(self) -> None:
        file_content = b"plain text content"
        response = client.post(
            "/upload",
            files={"file": ("test.txt", file_content, "text/plain")},
        )
        assert response.status_code == 400
        data = response.json()
        assert "Invalid file type" in data["detail"]

    def test_upload_empty_json_file(self) -> None:
        file_content = b""
        response = client.post(
            "/upload",
            files={"file": ("empty.json", file_content, "application/json")},
        )
        assert response.status_code == 400
        data = response.json()
        assert "Invalid JSON" in data["detail"]

    def test_upload_non_array_json(self) -> None:
        file_content = b'{"key": "value"}'
        response = client.post(
            "/upload",
            files={"file": ("test.json", file_content, "application/json")},
        )
        assert response.status_code == 400
        data = response.json()
        assert "Expected a JSON array" in data["detail"]

    def test_upload_empty_array(self) -> None:
        file_content = b"[]"
        response = client.post(
            "/upload",
            files={"file": ("test.json", file_content, "application/json")},
        )
        assert response.status_code == 400
        data = response.json()
        assert "empty" in data["detail"].lower()

    def test_upload_missing_fields(self) -> None:
        file_content = b'[{"symbol": "TEST"}]'
        response = client.post(
            "/upload",
            files={"file": ("test.json", file_content, "application/json")},
        )
        assert response.status_code == 400
        data = response.json()
        assert "Missing required fields" in data["detail"]

    def test_upload_no_file_returns_error(self) -> None:
        response = client.post("/upload")
        assert response.status_code == 422
