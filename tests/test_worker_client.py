from unittest.mock import AsyncMock, patch

import httpx
import pytest

from worker_client import WorkerError, process_with_worker


@pytest.mark.asyncio
async def test_process_with_worker_success() -> None:
    response_data = {
        "success": True,
        "data": {
            "symbol": "^AXJO",
            "name": "S&P/ASX 200",
            "price": 8950.56,
            "change": 9.885,
            "change_percent": 0.110507,
            "day_high": 8972.37,
            "day_low": 8926.7,
            "previous_close": 8940.68,
            "timestamp": "2026-01-28T12:42:18Z",
        },
    }
    mock_response = httpx.Response(200, json=response_data)

    with patch("worker_client.httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.post.return_value = mock_response
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_client.return_value = mock_instance

        records = [{"symbol": "^AXJO", "price": 100.0}]
        result = await process_with_worker(records)

        assert result["symbol"] == "^AXJO"
        assert result["price"] == 8950.56
        mock_instance.post.assert_called_once()


@pytest.mark.asyncio
async def test_process_with_worker_connection_error() -> None:
    with patch("worker_client.httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.post.side_effect = httpx.ConnectError("Connection refused")
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_client.return_value = mock_instance

        with pytest.raises(WorkerError) as exc_info:
            await process_with_worker([{"symbol": "TEST"}])

        assert "Worker unavailable" in str(exc_info.value)


@pytest.mark.asyncio
async def test_process_with_worker_error_response() -> None:
    response_data = {
        "success": False,
        "error": "input data cannot be empty",
    }
    mock_response = httpx.Response(200, json=response_data)

    with patch("worker_client.httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.post.return_value = mock_response
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_client.return_value = mock_instance

        with pytest.raises(WorkerError) as exc_info:
            await process_with_worker([])

        assert "input data cannot be empty" in str(exc_info.value)


@pytest.mark.asyncio
async def test_process_with_worker_non_200_status() -> None:
    mock_response = httpx.Response(500)

    with patch("worker_client.httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.post.return_value = mock_response
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_client.return_value = mock_instance

        with pytest.raises(WorkerError) as exc_info:
            await process_with_worker([{"symbol": "TEST"}])

        assert "status 500" in str(exc_info.value)
