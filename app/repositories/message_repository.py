"""CRUD de mensagens e conversas."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ConversationNotFoundError
from app.models.entities import Conversation, Message


class MessageRepository:
    """Repositório de conversas e mensagens."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_create_conversation(self, conversation_id: str | None) -> Conversation:
        """Obtém conversa existente ou cria nova."""
        if conversation_id:
            conversation = self.db.get(Conversation, conversation_id)
            if conversation:
                return conversation
            raise ConversationNotFoundError(f"Conversa {conversation_id} não encontrada")

        conversation = Conversation(id=str(uuid.uuid4()))
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def add_message(
        self,
        conversation: Conversation,
        content: str,
        role: str = "user",
        response_time_seconds: float | None = None,
    ) -> Message:
        """Adiciona mensagem à conversa."""
        message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation.id,
            content=content,
            role=role,
            response_time_seconds=response_time_seconds,
        )
        self.db.add(message)
        conversation.message_count += 1
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_user_messages(self, conversation_id: str) -> list[Message]:
        """Retorna mensagens do usuário em ordem cronológica."""
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id, Message.role == "user")
            .order_by(Message.created_at)
        )
        return list(self.db.scalars(stmt).all())

    def update_summary(self, conversation: Conversation, summary: str) -> None:
        """Atualiza resumo da conversa."""
        conversation.summary = summary
        self.db.commit()
