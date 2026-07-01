"""Schemas Pydantic para request/response da API."""

from datetime import datetime

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    """Payload para envio de mensagem no chat."""

    conversation_id: str | None = None
    content: str = Field(..., min_length=1, max_length=5000)
    response_time_seconds: float | None = Field(default=None, ge=0)


class AnalysisResult(BaseModel):
    """Resultado da análise de uma mensagem."""

    ia_called: bool
    call_reason: str
    rules_triggered: list[str]
    summary: str
    risco_de_churn: str | None = None
    confianca: float | None = None
    acao: str | None = None
    tokens_input: int = 0
    tokens_output: int = 0
    tokens_used: int = 0
    cost_usd: float = 0.0
    economy_registered: bool = False
    economy_usd: float = 0.0


class MessageResponse(BaseModel):
    """Resposta após processamento de mensagem."""

    conversation_id: str
    message_id: str
    bot_reply: str | None = None
    analysis: AnalysisResult


class DashboardMetrics(BaseModel):
    """Métricas agregadas do dashboard."""

    total_messages: int
    ai_calls: int
    ai_calls_avoided: int
    economy_percent: float
    tokens_used: int
    total_cost_usd: float
    total_economy_usd: float


class DecisionHistoryItem(BaseModel):
    """Item do histórico de decisões."""

    id: str
    conversation_id: str
    rules_triggered: list[str]
    ai_called: bool
    call_reason: str
    risco_de_churn: str | None
    confianca: float | None
    acao: str | None
    cost_usd: float
    economy_usd: float
    created_at: datetime


class AutomationHistoryItem(BaseModel):
    """Item do histórico de automações."""

    id: str
    decision_id: str
    action_type: str
    details: str
    created_at: datetime


class HealthResponse(BaseModel):
    """Resposta do health check."""

    status: str
    app_name: str
    version: str
