"""Orquestra log, persistência, sugestão e métricas de custo."""

import logging
import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.layers.ia.client import AIAnalysisResult
from app.models.entities import AutomationLog, Decision

logger = logging.getLogger(__name__)

HIGH_RISK_LEVELS = frozenset({"alto", "high"})


@dataclass
class AutomationResult:
    """Resultado do pipeline de automação."""

    bot_reply: str | None
    actions: list[str]


class AutomationPipeline:
    """Executa ações automáticas após análise de IA."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def run(
        self,
        decision: Decision,
        analysis: AIAnalysisResult | None,
    ) -> AutomationResult:
        """Executa pipeline completo de automação."""
        actions: list[str] = []
        bot_reply: str | None = None

        self._log_action(decision.id, "log_registered", "Análise registrada no sistema")
        actions.append("log_registered")

        if analysis is None:
            if decision.economy_registered:
                self._log_action(
                    decision.id,
                    "economy_saved",
                    f"Economia de ${decision.economy_usd:.6f} registrada",
                )
                actions.append("economy_saved")
            return AutomationResult(bot_reply=None, actions=actions)

        self._log_action(
            decision.id,
            "ai_cost_recorded",
            f"Custo: ${decision.cost_usd:.6f} | Tokens: "
            f"{decision.tokens_input}+{decision.tokens_output}",
        )
        actions.append("ai_cost_recorded")

        if analysis.risco_de_churn.lower() in HIGH_RISK_LEVELS:
            bot_reply = self._build_suggestion(analysis)
            self._log_action(
                decision.id,
                "suggestion_sent",
                f"Sugestão enviada: {analysis.acao}",
            )
            actions.append("suggestion_sent")
            logger.warning(
                "Risco alto detectado | decisão=%s | ação=%s",
                decision.id,
                analysis.acao,
            )

        return AutomationResult(bot_reply=bot_reply, actions=actions)

    def _build_suggestion(self, analysis: AIAnalysisResult) -> str:
        """Monta mensagem automática para o cliente."""
        return (
            f"⚠️ Detectamos sinais de insatisfação. "
            f"Sugestão: {analysis.acao} "
            f"(confiança: {analysis.confianca:.0%})"
        )

    def _log_action(self, decision_id: str, action_type: str, details: str) -> None:
        """Persiste log de automação."""
        log = AutomationLog(
            id=str(uuid.uuid4()),
            decision_id=decision_id,
            action_type=action_type,
            details=details,
        )
        self.db.add(log)
        self.db.commit()
