"""Motor que executa as regras e retorna quais foram acionadas."""

from dataclasses import dataclass

from app.layers.vigia.rules import (
    RuleResult,
    check_delay,
    check_keywords,
    check_short_message,
)


@dataclass
class VigiaResult:
    """Resultado consolidado da camada Vigia."""

    rules: list[RuleResult]
    any_triggered: bool
    triggered_names: list[str]

    @property
    def triggered_details(self) -> list[str]:
        """Retorna detalhes apenas das regras acionadas."""
        return [r.detail for r in self.rules if r.triggered]


def run_vigia(content: str, response_time_seconds: float | None) -> VigiaResult:
    """Executa todas as regras do Vigia sobre uma mensagem."""
    results = [
        check_delay(response_time_seconds),
        check_short_message(content),
        check_keywords(content),
    ]
    triggered = [r.name for r in results if r.triggered]
    return VigiaResult(
        rules=results,
        any_triggered=len(triggered) > 0,
        triggered_names=triggered,
    )
