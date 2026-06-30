"""Dependências injetáveis do FastAPI."""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.models.database import get_db

__all__ = ["get_db_session"]


def get_db_session() -> Generator[Session, None, None]:
    """Alias para injeção de sessão."""
    yield from get_db()
