"""Ponto de entrada da aplicação FastAPI."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.api.routes import chat, dashboard, health
from app.config import get_settings
from app.core.logging_config import setup_logging
from app.models.database import init_db

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Ciclo de vida da aplicação."""
    setup_logging()
    init_db()
    yield


def create_app() -> FastAPI:
    """Factory da aplicação FastAPI."""
    settings = get_settings()

    application = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Plataforma inteligente de detecção de churn com IA sob demanda",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health.router)
    application.include_router(chat.router)
    application.include_router(dashboard.router)

    if FRONTEND_DIR.exists():
        application.mount(
            "/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend"
        )

    return application


app = create_app()
