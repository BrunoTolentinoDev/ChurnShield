"""Persistência de métricas, custos e economia."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.entities import AutomationLog, Decision, Message


class MetricsRepository:
    """Consultas agregadas para métricas do dashboard."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def total_messages(self) -> int:
        """Total de mensagens de usuário."""
        stmt = select(func.count()).select_from(Message).where(Message.role == "user")
        return self.db.scalar(stmt) or 0

    def ai_calls(self) -> int:
        """Quantidade de chamadas à IA."""
        stmt = select(func.count()).select_from(Decision).where(Decision.ai_called.is_(True))
        return self.db.scalar(stmt) or 0

    def ai_calls_avoided(self) -> int:
        """Quantidade de análises sem chamada à IA."""
        stmt = (
            select(func.count())
            .select_from(Decision)
            .where(Decision.ai_called.is_(False))
        )
        return self.db.scalar(stmt) or 0

    def total_tokens(self) -> int:
        """Soma de tokens utilizados."""
        stmt = select(
            func.coalesce(func.sum(Decision.tokens_input + Decision.tokens_output), 0)
        )
        return int(self.db.scalar(stmt) or 0)

    def total_cost(self) -> float:
        """Custo total em USD."""
        stmt = select(func.coalesce(func.sum(Decision.cost_usd), 0.0))
        return float(self.db.scalar(stmt) or 0.0)

    def total_economy(self) -> float:
        """Economia total em USD."""
        stmt = select(func.coalesce(func.sum(Decision.economy_usd), 0.0))
        return float(self.db.scalar(stmt) or 0.0)

    def list_automations(self, limit: int = 50) -> list[AutomationLog]:
        """Lista automações recentes."""
        stmt = (
            select(AutomationLog)
            .order_by(AutomationLog.created_at.desc())
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())
