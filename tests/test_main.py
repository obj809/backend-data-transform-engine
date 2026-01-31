import os
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app
from middleware import DEFAULT_CORS_ORIGINS, get_cors_origins
from worker_client import WorkerError

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
        mock_result = {
            "symbol": "^AXJO",
            "name": "S&P/ASX 200",
            "price": 8950.56,
            "change": 9.885,
            "change_percent": 0.110507,
            "day_high": 8972.37,
            "day_low": 8926.7,
            "previous_close": 8940.68,
            "timestamp": "2026-01-28T12:42:18Z",
        }
        file_content = b"""[
            {
                "symbol": "^AXJO",
                "name": "S&P/ASX 200",
                "price": 8929.41,
                "change": 7.53,
                "change_percent": 0.084399,
                "day_high": 8948.55,
                "day_low": 8903.81,
                "previous_close": 8921.88
            }
        ]"""
        with patch("main.process_with_worker", new_callable=AsyncMock) as mock_worker:
            mock_worker.return_value = mock_result
            response = client.post(
                "/upload",
                files={"file": ("test.json", file_content, "application/json")},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "^AXJO"
        assert data["name"] == "S&P/ASX 200"
        assert data["price"] == 8950.56

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
        with patch("main.process_with_worker", new_callable=AsyncMock) as mock_worker:
            mock_worker.side_effect = WorkerError("input data cannot be empty")
            response = client.post(
                "/upload",
                files={"file": ("test.json", file_content, "application/json")},
            )
        assert response.status_code == 503

    def test_upload_missing_fields(self) -> None:
        file_content = b'[{"symbol": "TEST"}]'
        with patch("main.process_with_worker", new_callable=AsyncMock) as mock_worker:
            mock_worker.side_effect = WorkerError("Missing required fields")
            response = client.post(
                "/upload",
                files={"file": ("test.json", file_content, "application/json")},
            )
        assert response.status_code == 503

    def test_upload_no_file_returns_error(self) -> None:
        response = client.post("/upload")
        assert response.status_code == 422

    def test_upload_worker_unavailable(self) -> None:
        file_content = b'[{"symbol": "TEST", "name": "Test", "price": 100}]'
        with patch("main.process_with_worker", new_callable=AsyncMock) as mock_worker:
            mock_worker.side_effect = WorkerError("Worker unavailable")
            response = client.post(
                "/upload",
                files={"file": ("test.json", file_content, "application/json")},
            )
        assert response.status_code == 503
        assert "Worker unavailable" in response.json()["detail"]
