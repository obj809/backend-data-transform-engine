import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://172.20.10.2:3000",
]


def get_cors_origins() -> list[str]:
    """Get CORS origins from environment variable or use defaults.

    The CORS_ORIGINS environment variable should contain comma-separated URLs.
    If not set or empty, returns the default origins.
    """
    cors_env = os.environ.get("CORS_ORIGINS", "")
    if not cors_env.strip():
        return DEFAULT_CORS_ORIGINS.copy()

    origins = [origin.strip() for origin in cors_env.split(",")]
    return [origin for origin in origins if origin]


def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
