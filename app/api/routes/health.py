"""Endpoint de health check."""

from fastapi import APIRouter

from app import __version__
from app.config import get_settings
from app.models.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Verifica se a API está operacional."""
    settings = get_settings()
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=__version__,
    )
