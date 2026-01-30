from fastapi import FastAPI

from middleware import setup_cors

app = FastAPI()
setup_cors(app)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
