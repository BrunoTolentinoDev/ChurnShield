"""Endpoints do chat e análise de mensagens."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.models.schemas import MessageCreate, MessageResponse
from app.services.message_service import MessageService

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/message", response_model=MessageResponse)
def send_message(
    payload: MessageCreate,
    db: Session = Depends(get_db_session),
) -> MessageResponse:
    """Recebe mensagem do chat e executa pipeline de análise."""
    service = MessageService(db)
    return service.process_message(payload)
