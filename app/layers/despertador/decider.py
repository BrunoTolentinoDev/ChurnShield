"""Lógica de decisão com base no resultado do Vigia."""

from dataclasses import dataclass

from app.layers.vigia.engine import VigiaResult


@dataclass
class DespertadorResult:
    """Decisão do Despertador sobre chamar a IA."""

    should_call_ai: bool
    reason: str
    economy_registered: bool = False


def decide(vigia_result: VigiaResult) -> DespertadorResult:
    """
    Decide se a IA deve ser chamada.

    Sem regras acionadas → não chama IA e registra economia.
  Com regras acionadas → chama IA para análise aprofundada.
    """
    if not vigia_result.any_triggered:
        return DespertadorResult(
            should_call_ai=False,
            reason="Nenhuma regra acionada — IA não necessária",
            economy_registered=True,
        )

    details = "; ".join(vigia_result.triggered_details)
    return DespertadorResult(
        should_call_ai=True,
        reason=f"Regras acionadas: {', '.join(vigia_result.triggered_names)}. {details}",
        economy_registered=False,
    )
