import json
import logging
from typing import Any

from fastapi import FastAPI, HTTPException, UploadFile

from middleware import setup_cors
from worker_client import WorkerError, process_with_worker

logger = logging.getLogger(__name__)

app = FastAPI()
setup_cors(app)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/upload")
async def upload_file(file: UploadFile) -> dict[str, Any]:
    if not file.filename or not file.filename.endswith(".json"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only JSON files are accepted."
        )

    contents = await file.read()

    try:
        data = json.loads(contents)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}") from None

    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="Expected a JSON array of records")

    try:
        result = await process_with_worker(data)
        return result
    except WorkerError as e:
        logger.warning("Worker processing failed: %s", e)
        raise HTTPException(status_code=503, detail="Worker unavailable") from None
