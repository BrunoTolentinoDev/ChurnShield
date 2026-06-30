"""Agregação de métricas para o dashboard."""

from sqlalchemy.orm import Session

from app.models.schemas import AutomationHistoryItem, DashboardMetrics, DecisionHistoryItem
from app.repositories.decision_repository import DecisionRepository
from app.repositories.metrics_repository import MetricsRepository


class DashboardService:
    """Serviço de métricas e históricos."""

    def __init__(self, db: Session) -> None:
        self.metrics_repo = MetricsRepository(db)
        self.decision_repo = DecisionRepository(db)

    def get_metrics(self) -> DashboardMetrics:
        """Retorna métricas agregadas."""
        total = self.metrics_repo.total_messages()
        ai_calls = self.metrics_repo.ai_calls()
        avoided = self.metrics_repo.ai_calls_avoided()
        total_decisions = ai_calls + avoided
        economy_percent = (avoided / total_decisions * 100) if total_decisions else 0.0

        return DashboardMetrics(
            total_messages=total,
            ai_calls=ai_calls,
            ai_calls_avoided=avoided,
            economy_percent=round(economy_percent, 2),
            tokens_used=self.metrics_repo.total_tokens(),
            total_cost_usd=round(self.metrics_repo.total_cost(), 6),
            total_economy_usd=round(self.metrics_repo.total_economy(), 6),
        )

    def get_decision_history(self, limit: int = 50) -> list[DecisionHistoryItem]:
        """Retorna histórico de decisões."""
        decisions = self.decision_repo.list_recent(limit)
        return [
            DecisionHistoryItem(
                id=d.id,
                conversation_id=d.conversation_id,
                rules_triggered=DecisionRepository.parse_rules(d),
                ai_called=d.ai_called,
                call_reason=d.call_reason,
                risco_de_churn=d.risco_de_churn,
                confianca=d.confianca,
                acao=d.acao,
                cost_usd=d.cost_usd,
                economy_usd=d.economy_usd,
                created_at=d.created_at,
            )
            for d in decisions
        ]

    def get_automation_history(self, limit: int = 50) -> list[AutomationHistoryItem]:
        """Retorna histórico de automações."""
        logs = self.metrics_repo.list_automations(limit)
        return [
            AutomationHistoryItem(
                id=log.id,
                decision_id=log.decision_id,
                action_type=log.action_type,
                details=log.details,
                created_at=log.created_at,
            )
            for log in logs
        ]
