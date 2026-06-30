"""Conexão e sessão SQLAlchemy com SQLite."""

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    """Classe base para entidades ORM."""


def _ensure_data_dir(database_url: str) -> None:
    """Garante que o diretório do SQLite exista."""
    if database_url.startswith("sqlite:///"):
        db_path = Path(database_url.replace("sqlite:///", ""))
        db_path.parent.mkdir(parents=True, exist_ok=True)


settings = get_settings()
_ensure_data_dir(settings.database_url)

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """Fornece sessão de banco para injeção de dependência."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Cria todas as tabelas no banco."""
    from app.models import entities  # noqa: F401

    Base.metadata.create_all(bind=engine)
