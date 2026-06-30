"""Exceções de domínio customizadas."""


class ChurnShieldError(Exception):
    """Erro base da aplicação."""


class ConversationNotFoundError(ChurnShieldError):
    """Conversa não encontrada no banco."""


class AIClientError(ChurnShieldError):
    """Falha na comunicação com a API de IA."""


class AIResponseParseError(ChurnShieldError):
    """Resposta da IA não está no formato JSON esperado."""
