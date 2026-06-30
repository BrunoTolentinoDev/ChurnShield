"""Gera e atualiza resumo a cada N mensagens."""

from dataclasses import dataclass

from app.config import get_settings


@dataclass
class MemoriaResult:
    """Estado da memória inteligente após processamento."""

    summary: str
    updated: bool


def _build_summary(messages: list[str], previous_summary: str) -> str:
    """Constrói resumo incremental a partir das mensagens."""
    if not messages:
        return previous_summary

    recent = " | ".join(messages[-10:])
    if previous_summary:
        return f"{previous_summary} → {recent}"
    return recent


def update_summary(
    previous_summary: str,
    message_contents: list[str],
    message_count: int,
) -> MemoriaResult:
    """
    Atualiza resumo a cada N mensagens (configurável).

    Retorna o resumo atual (atualizado ou anterior).
    """
    interval = get_settings().memoria_summary_interval
    should_update = message_count > 0 and message_count % interval == 0

    if should_update:
        return MemoriaResult(
            summary=_build_summary(message_contents, previous_summary),
            updated=True,
        )

    if not previous_summary and message_contents:
        return MemoriaResult(
            summary=_build_summary(message_contents[:1], ""),
            updated=True,
        )

    return MemoriaResult(summary=previous_summary, updated=False)


def get_context_for_ai(summary: str, last_message: str) -> dict[str, str]:
    """Retorna apenas resumo e última mensagem para envio à IA."""
    return {"resumo": summary, "ultima_mensagem": last_message}
