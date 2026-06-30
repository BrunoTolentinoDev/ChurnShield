"""Tabelas do banco: mensagens, decisões, automações e métricas."""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Conversation(Base):
  """Representa uma conversa de chat."""

  __tablename__ = "conversations"

  id: Mapped[str] = mapped_column(String(36), primary_key=True)
  summary: Mapped[str] = mapped_column(Text, default="")
  message_count: Mapped[int] = mapped_column(Integer, default=0)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
  updated_at: Mapped[datetime] = mapped_column(
      DateTime, default=_utcnow, onupdate=_utcnow
  )

  messages: Mapped[list["Message"]] = relationship(back_populates="conversation")
  decisions: Mapped[list["Decision"]] = relationship(back_populates="conversation")


class Message(Base):
  """Mensagem enviada pelo cliente ou sistema."""

  __tablename__ = "messages"

  id: Mapped[str] = mapped_column(String(36), primary_key=True)
  conversation_id: Mapped[str] = mapped_column(
      String(36), ForeignKey("conversations.id")
  )
  role: Mapped[str] = mapped_column(String(20), default="user")
  content: Mapped[str] = mapped_column(Text)
  response_time_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)

  conversation: Mapped["Conversation"] = relationship(back_populates="messages")
  decision: Mapped["Decision | None"] = relationship(back_populates="message")


class Decision(Base):
  """Registro de decisão do Despertador e resultado da IA."""

  __tablename__ = "decisions"

  id: Mapped[str] = mapped_column(String(36), primary_key=True)
  conversation_id: Mapped[str] = mapped_column(
      String(36), ForeignKey("conversations.id")
  )
  message_id: Mapped[str] = mapped_column(String(36), ForeignKey("messages.id"))
  rules_triggered: Mapped[str] = mapped_column(Text, default="[]")
  should_call_ai: Mapped[bool] = mapped_column(Boolean, default=False)
  call_reason: Mapped[str] = mapped_column(Text, default="")
  ai_called: Mapped[bool] = mapped_column(Boolean, default=False)
  economy_registered: Mapped[bool] = mapped_column(Boolean, default=False)
  economy_usd: Mapped[float] = mapped_column(Float, default=0.0)
  summary_snapshot: Mapped[str] = mapped_column(Text, default="")
  risco_de_churn: Mapped[str | None] = mapped_column(String(20), nullable=True)
  confianca: Mapped[float | None] = mapped_column(Float, nullable=True)
  acao: Mapped[str | None] = mapped_column(Text, nullable=True)
  tokens_input: Mapped[int] = mapped_column(Integer, default=0)
  tokens_output: Mapped[int] = mapped_column(Integer, default=0)
  cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)

  conversation: Mapped["Conversation"] = relationship(back_populates="decisions")
  message: Mapped["Message"] = relationship(back_populates="decision")
  automations: Mapped[list["AutomationLog"]] = relationship(
      back_populates="decision"
  )


class AutomationLog(Base):
  """Histórico de ações automáticas executadas."""

  __tablename__ = "automation_logs"

  id: Mapped[str] = mapped_column(String(36), primary_key=True)
  decision_id: Mapped[str] = mapped_column(String(36), ForeignKey("decisions.id"))
  action_type: Mapped[str] = mapped_column(String(50))
  details: Mapped[str] = mapped_column(Text, default="")
  created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)

  decision: Mapped["Decision"] = relationship(back_populates="automations")
