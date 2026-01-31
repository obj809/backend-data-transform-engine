import json
from typing import Any

from fastapi import FastAPI, HTTPException, UploadFile

from middleware import setup_cors
from processor import process_stock_data

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
        result = process_stock_data(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from None

    return result
