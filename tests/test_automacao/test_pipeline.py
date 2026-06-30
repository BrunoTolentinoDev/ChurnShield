"""Testes do pipeline de automação."""

import uuid

from app.layers.automacao.pipeline import AutomationPipeline
from app.layers.ia.client import AIAnalysisResult
from app.models.entities import Decision


class TestAutomacao:
    def test_economy_automation(self, db_session) -> None:
        decision = Decision(
            id=str(uuid.uuid4()),
            conversation_id=str(uuid.uuid4()),
            message_id=str(uuid.uuid4()),
            economy_registered=True,
            economy_usd=0.001,
        )
        db_session.add(decision)
        db_session.commit()

        pipeline = AutomationPipeline(db_session)
        result = pipeline.run(decision, None)

        assert "log_registered" in result.actions
        assert "economy_saved" in result.actions
        assert result.bot_reply is None

    def test_high_risk_sends_suggestion(self, db_session) -> None:
        decision = Decision(
            id=str(uuid.uuid4()),
            conversation_id=str(uuid.uuid4()),
            message_id=str(uuid.uuid4()),
            cost_usd=0.002,
            tokens_input=100,
            tokens_output=50,
        )
        db_session.add(decision)
        db_session.commit()

        analysis = AIAnalysisResult(
            risco_de_churn="alto",
            confianca=0.93,
            acao="oferecer 15% de desconto",
            tokens_input=100,
            tokens_output=50,
            raw_response="{}",
        )

        pipeline = AutomationPipeline(db_session)
        result = pipeline.run(decision, analysis)

        assert result.bot_reply is not None
        assert "suggestion_sent" in result.actions
        assert "15%" in result.bot_reply or "desconto" in result.bot_reply.lower()
