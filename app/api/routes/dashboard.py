"""Endpoints de métricas e histórico para o dashboard."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.models.schemas import (
    AutomationHistoryItem,
    DashboardMetrics,
    DecisionHistoryItem,
)
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/metrics", response_model=DashboardMetrics)
def get_metrics(db: Session = Depends(get_db_session)) -> DashboardMetrics:
    """Retorna métricas agregadas do sistema."""
    return DashboardService(db).get_metrics()


@router.get("/history/decisions", response_model=list[DecisionHistoryItem])
def get_decision_history(
    limit: int = 50,
    db: Session = Depends(get_db_session),
) -> list[DecisionHistoryItem]:
    """Retorna histórico de decisões."""
    return DashboardService(db).get_decision_history(limit)


@router.get("/history/automations", response_model=list[AutomationHistoryItem])
def get_automation_history(
    limit: int = 50,
    db: Session = Depends(get_db_session),
) -> list[AutomationHistoryItem]:
    """Retorna histórico de automações."""
    return DashboardService(db).get_automation_history(limit)
