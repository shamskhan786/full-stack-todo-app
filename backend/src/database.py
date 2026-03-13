from collections.abc import Generator

from sqlalchemy.pool import NullPool
from sqlmodel import Session, create_engine

from .config import settings
from .models.conversation import ConversationMessage, ConversationSession  # noqa: F401 — imported for SQLModel.metadata.create_all discovery
from .models.task import Task  # noqa: F401 — imported for SQLModel.metadata.create_all discovery

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,
    echo=settings.ENVIRONMENT == "development",
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
