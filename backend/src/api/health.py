import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import text

from ..database import engine

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health_check() -> JSONResponse:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return JSONResponse(
            status_code=200,
            content={"status": "healthy", "database": "connected"},
        )
    except Exception:
        logger.exception("Health check: database unreachable")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected"},
        )
