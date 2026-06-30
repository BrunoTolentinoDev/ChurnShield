"""Fixtures compartilhadas do Pytest."""

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["MOCK_AI"] = "true"
os.environ["DATABASE_URL"] = "sqlite://"

from app.config import get_settings
from app.models import entities  # noqa: F401 — registra tabelas no metadata
from app.api.dependencies import get_db_session
from app.models.database import Base, get_db
from app.main import app

get_settings.cache_clear()


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Sessão de banco em memória para testes."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Cliente de teste com banco injetado."""

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_db_session] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
