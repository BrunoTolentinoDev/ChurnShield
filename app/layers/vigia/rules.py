"""Definição das regras de detecção (palavras-chave, tempo, tamanho)."""

from dataclasses import dataclass

from app.config import get_settings

CHURN_KEYWORDS: tuple[str, ...] = (
    "cancelar",
    "caro",
    "concorrente",
    "depois",
    "reembolso",
    "insatisfeito",
)


@dataclass(frozen=True)
class RuleResult:
    """Resultado da avaliação de uma regra."""

    name: str
    triggered: bool
    detail: str


def check_delay(response_time_seconds: float | None) -> RuleResult:
    """Verifica demora superior ao limite configurado."""
    threshold = get_settings().vigia_delay_threshold_seconds
    if response_time_seconds is None:
        return RuleResult("delay", False, "Tempo de resposta não informado")
    triggered = response_time_seconds > threshold
    detail = (
        f"Demora de {response_time_seconds:.1f}s (limite: {threshold}s)"
        if triggered
        else f"Tempo OK ({response_time_seconds:.1f}s)"
    )
    return RuleResult("delay", triggered, detail)


def check_short_message(content: str) -> RuleResult:
    """Verifica se a mensagem é muito curta."""
    min_len = get_settings().vigia_min_message_length
    length = len(content.strip())
    triggered = length < min_len
    detail = (
        f"Mensagem curta ({length} chars, mínimo: {min_len})"
        if triggered
        else f"Tamanho OK ({length} chars)"
    )
    return RuleResult("short_message", triggered, detail)


def check_keywords(content: str) -> RuleResult:
    """Verifica palavras-chave de risco de churn."""
    lowered = content.lower()
    found = [word for word in CHURN_KEYWORDS if word in lowered]
    triggered = len(found) > 0
    detail = (
        f"Palavras detectadas: {', '.join(found)}"
        if triggered
        else "Nenhuma palavra-chave detectada"
    )
    return RuleResult("keywords", triggered, detail)
