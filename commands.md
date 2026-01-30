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
