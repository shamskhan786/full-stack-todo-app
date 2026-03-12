import os
from collections.abc import Generator

# Set test environment BEFORE importing app modules
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("JWKS_URL", "http://localhost:3000/api/auth/jwks")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")
os.environ.setdefault("ENVIRONMENT", "test")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlmodel import Session, SQLModel, create_engine  # noqa: E402

from src.dependencies import get_session, verify_jwt  # noqa: E402
from src.main import app  # noqa: E402

# Fixed UUIDs for deterministic tests
TEST_USER_ID = "11111111-1111-1111-1111-111111111111"
OTHER_USER_ID = "22222222-2222-2222-2222-222222222222"

engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False},
)


def override_get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)
    app.dependency_overrides.clear()


@pytest.fixture()
def client() -> TestClient:
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[verify_jwt] = lambda: {"sub": TEST_USER_ID}
    return TestClient(app)


@pytest.fixture()
def client_other_user() -> TestClient:
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[verify_jwt] = lambda: {"sub": OTHER_USER_ID}
    return TestClient(app)


@pytest.fixture()
def client_no_auth() -> TestClient:
    app.dependency_overrides[get_session] = override_get_session
    # Do NOT override verify_jwt — let it require real auth
    if verify_jwt in app.dependency_overrides:
        del app.dependency_overrides[verify_jwt]
    return TestClient(app)
