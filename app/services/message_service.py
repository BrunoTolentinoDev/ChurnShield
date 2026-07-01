"""Fluxo principal: recebe mensagem → camadas → resposta."""

import logging

from sqlalchemy.orm import Session

from app.layers.automacao.pipeline import AutomationPipeline
from app.layers.despertador.decider import decide
from app.layers.ia.client import AIAnalysisResult, DeepSeekClient
from app.layers.memoria.summarizer import get_context_for_ai, update_summary
from app.layers.vigia.engine import run_vigia
from app.models.schemas import AnalysisResult, MessageCreate, MessageResponse
from app.repositories.decision_repository import DecisionRepository
from app.repositories.message_repository import MessageRepository
from app.services.cost_service import calculate_cost, estimate_avoided_cost

logger = logging.getLogger(__name__)


class MessageService:
    """Orquestra as 5 camadas de inteligência do ChurnShield."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.message_repo = MessageRepository(db)
        self.decision_repo = DecisionRepository(db)
        self.ai_client = DeepSeekClient()
        self.automation = AutomationPipeline(db)

    def process_message(self, payload: MessageCreate) -> MessageResponse:
        """Processa mensagem pelo pipeline completo."""
        conversation = self.message_repo.get_or_create_conversation(
            payload.conversation_id
        )
        message = self.message_repo.add_message(
            conversation,
            payload.content,
            response_time_seconds=payload.response_time_seconds,
        )

        user_messages = self.message_repo.get_user_messages(conversation.id)
        contents = [m.content for m in user_messages]

        memoria = update_summary(
            conversation.summary,
            contents,
            conversation.message_count,
        )
        if memoria.updated:
            self.message_repo.update_summary(conversation, memoria.summary)
            conversation.summary = memoria.summary

        vigia = run_vigia(payload.content, payload.response_time_seconds)
        despertador = decide(vigia)

        analysis: AIAnalysisResult | None = None
        economy_usd = 0.0
        tokens_in = tokens_out = 0
        cost_usd = 0.0
        ia_called = False

        if despertador.should_call_ai:
            context = get_context_for_ai(memoria.summary, payload.content)
            logger.info("Chamando IA | conversa=%s", conversation.id)
            analysis = self.ai_client.analyze(
                context["resumo"], context["ultima_mensagem"]
            )
            ia_called = True
            tokens_in = analysis.tokens_input
            tokens_out = analysis.tokens_output
            cost_usd = calculate_cost(tokens_in, tokens_out)
        elif despertador.economy_registered:
            tokens_in, tokens_out, economy_usd = estimate_avoided_cost(
                memoria.summary, payload.content
            )
            logger.info(
                "Economia registrada | conversa=%s | $%.6f",
                conversation.id,
                economy_usd,
            )

        decision = self.decision_repo.create(
            conversation_id=conversation.id,
            message_id=message.id,
            rules_triggered=vigia.triggered_names,
            should_call_ai=despertador.should_call_ai,
            call_reason=despertador.reason,
            ai_called=ia_called,
            economy_registered=despertador.economy_registered,
            economy_usd=economy_usd,
            summary_snapshot=memoria.summary,
            risco_de_churn=analysis.risco_de_churn if analysis else None,
            confianca=analysis.confianca if analysis else None,
            acao=analysis.acao if analysis else None,
            tokens_input=tokens_in,
            tokens_output=tokens_out,
            cost_usd=cost_usd,
        )

        automation = self.automation.run(decision, analysis)

        if automation.bot_reply:
            self.message_repo.add_message(
                conversation, automation.bot_reply, role="bot"
            )

        return MessageResponse(
            conversation_id=conversation.id,
            message_id=message.id,
            bot_reply=automation.bot_reply,
            analysis=AnalysisResult(
                ia_called=ia_called,
                call_reason=despertador.reason,
                rules_triggered=vigia.triggered_names,
                summary=memoria.summary,
                risco_de_churn=analysis.risco_de_churn if analysis else None,
                confianca=analysis.confianca if analysis else None,
                acao=analysis.acao if analysis else None,
                tokens_input=tokens_in,
                tokens_output=tokens_out,
                tokens_used=tokens_in + tokens_out,
                cost_usd=cost_usd,
                economy_registered=despertador.economy_registered,
                economy_usd=economy_usd,
            ),
        )
