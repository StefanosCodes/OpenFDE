from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api import v1_router
from app.database import SessionLocal
from app.exceptions import ConflictError, ResourceNotFoundError
from app.pagination import InvalidCursorError
from app.schemas import HealthResponse

app = FastAPI(
    title="OpenFDE Nexus",
    version="0.1.0",
    description="A lightweight customer-intelligence sandbox for OpenFDE agents.",
)


@app.exception_handler(ResourceNotFoundError)
def handle_not_found(_request: Request, exc: ResourceNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.exception_handler(ConflictError)
def handle_conflict(_request: Request, exc: ConflictError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})


@app.exception_handler(InvalidCursorError)
def handle_invalid_cursor(_request: Request, exc: InvalidCursorError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": str(exc)},
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": HealthResponse}},
    operation_id="health",
    tags=["system"],
)
def health() -> HealthResponse | JSONResponse:
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unavailable", "database": "unavailable"},
        )
    return HealthResponse(status="ready", database="ready")


app.include_router(v1_router)
