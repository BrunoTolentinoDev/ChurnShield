"""Histórico de decisões do Despertador e resultados da IA."""

import json
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Decision


class DecisionRepository:
    """Repositório de decisões de análise."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        conversation_id: str,
        message_id: str,
        rules_triggered: list[str],
        should_call_ai: bool,
        call_reason: str,
        ai_called: bool,
        economy_registered: bool,
        economy_usd: float,
        summary_snapshot: str,
        risco_de_churn: str | None = None,
        confianca: float | None = None,
        acao: str | None = None,
        tokens_input: int = 0,
        tokens_output: int = 0,
        cost_usd: float = 0.0,
    ) -> Decision:
        """Persiste decisão de análise."""
        decision = Decision(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            message_id=message_id,
            rules_triggered=json.dumps(rules_triggered, ensure_ascii=False),
            should_call_ai=should_call_ai,
            call_reason=call_reason,
            ai_called=ai_called,
            economy_registered=economy_registered,
            economy_usd=economy_usd,
            summary_snapshot=summary_snapshot,
            risco_de_churn=risco_de_churn,
            confianca=confianca,
            acao=acao,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            cost_usd=cost_usd,
        )
        self.db.add(decision)
        self.db.commit()
        self.db.refresh(decision)
        return decision

    def list_recent(self, limit: int = 50) -> list[Decision]:
        """Lista decisões mais recentes."""
        stmt = select(Decision).order_by(Decision.created_at.desc()).limit(limit)
        return list(self.db.scalars(stmt).all())

    @staticmethod
    def parse_rules(decision: Decision) -> list[str]:
        """Converte JSON de regras em lista."""
        try:
            return json.loads(decision.rules_triggered)
        except json.JSONDecodeError:
            return []
