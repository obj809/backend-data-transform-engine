"""Client for communicating with the Go worker service."""

import os
from typing import Any

import httpx

WORKER_URL = os.getenv("WORKER_URL", "http://localhost:8080")
WORKER_TIMEOUT = float(os.getenv("WORKER_TIMEOUT", "30.0"))


class WorkerError(Exception):
    """Raised when the worker service returns an error or is unavailable."""

    pass


async def process_with_worker(records: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Send stock records to the Go worker for processing.

    Args:
        records: List of stock data records.

    Returns:
        Aggregated result from the worker.

    Raises:
        WorkerError: If the worker is unavailable or returns an error.
    """
    async with httpx.AsyncClient(timeout=WORKER_TIMEOUT) as client:
        try:
            response = await client.post(
                f"{WORKER_URL}/process",
                json={"records": records},
            )
        except httpx.RequestError as e:
            raise WorkerError(f"Worker unavailable: {e}") from e

        if response.status_code != 200:
            raise WorkerError(f"Worker returned status {response.status_code}")

        data: dict[str, Any] = response.json()
        if not data.get("success"):
            raise WorkerError(data.get("error", "Unknown worker error"))

        result: dict[str, Any] = data["data"]
        return result
