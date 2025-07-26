import tomllib
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.models.common import PingResponse

# Import service routers
from src.routers import todo_v1


# Read version from pyproject.toml
def get_version() -> str:
    """Read version from pyproject.toml file."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomllib.load(f)
    return pyproject_data["project"]["version"]

app = FastAPI(
    title="Multi-Service API",
    description="A FastAPI server with independent service-level versioning",
    version=get_version(),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Include service routers - each service can be at different versions
app.include_router(todo_v1.router)  # /todo/v1/* - todo service


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to docs."""
    return RedirectResponse(url="/docs")


@app.get("/ping", response_model=PingResponse, summary="Ping the API to check status")
async def ping():
    """
    A simple endpoint to verify that the API is running.
    Returns a status message and a 200 HTTP status code.
    """
    return PingResponse(message="pong", status="ok", timestamp=datetime.utcnow())
