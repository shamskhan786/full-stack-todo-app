import logging
import logging.config
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, text

from .api.router import api_router
from .config import settings
from .database import engine
from .mcp import mcp
from .mcp import tools  # noqa: F401 — import to register MCP tools
from .schemas.responses import ErrorDetail, ErrorResponse

# Configure structured logging for traceability
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "structured": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "structured",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "backend": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "backend.mcp": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "backend.agents": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "backend.api": {"level": "INFO", "handlers": ["console"], "propagate": False},
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}
logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)

# Create MCP HTTP app once (shared between lifespan and mount)
mcp_app = mcp.http_app(path="/")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting backend self-healing checks...")

    # Auto-create missing database tables (idempotent — no-op if tables exist)
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables verified/created successfully")
    except Exception:
        logger.exception("Failed to create database tables")

    # Validate database connectivity
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connectivity: OK")
    except Exception:
        logger.exception("Database connectivity check failed")

    # Initialize FastMCP's streamable HTTP session manager (required for task group)
    async with mcp_app.lifespan(mcp_app):
        logger.info("MCP server initialized")
        logger.info("Backend startup complete")
        yield


app = FastAPI(
    title="Todo Full-Stack Web Application API",
    version="1.0.0",
    description="RESTful API for managing user tasks with JWT authentication",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "*"],  # Allow OpenAI infrastructure to reach /mcp
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    details = []
    for err in exc.errors():
        field = str(err["loc"][-1]) if err["loc"] else "unknown"
        details.append(ErrorDetail(field=field, message=err["msg"]))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="Validation failed",
            code="VALIDATION_ERROR",
            details=details,
        ).model_dump(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            code=str(exc.status_code),
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            code="INTERNAL_ERROR",
        ).model_dump(),
    )


app.include_router(api_router)

# Mount MCP server at /mcp endpoint
app.mount("/mcp", mcp_app)
