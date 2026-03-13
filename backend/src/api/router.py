from fastapi import APIRouter

from .chat import router as chat_router
from .conversations import router as conversations_router
from .health import router as health_router
from .tasks import router as tasks_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router)
api_router.include_router(tasks_router)
api_router.include_router(conversations_router)
api_router.include_router(chat_router)
