"""Utilitários de cálculo de custo e economia."""

from app.config import Settings, get_settings
from app.layers.ia.client import estimate_tokens
from app.layers.ia.prompts import SYSTEM_PROMPT, build_user_prompt


def calculate_cost(
    tokens_input: int,
    tokens_output: int,
    settings: Settings | None = None,
) -> float:
    """Calcula custo em USD com base nos tokens."""
    cfg = settings or get_settings()
    input_cost = (tokens_input / 1_000_000) * cfg.cost_per_million_input_tokens
    output_cost = (tokens_output / 1_000_000) * cfg.cost_per_million_output_tokens
    return round(input_cost + output_cost, 6)


def estimate_avoided_cost(
    resumo: str,
    ultima_mensagem: str,
    settings: Settings | None = None,
) -> tuple[int, int, float]:
    """Estima tokens e custo que seriam gastos se a IA fosse chamada."""
    user_prompt = build_user_prompt(resumo, ultima_mensagem)
    tokens_in = estimate_tokens(SYSTEM_PROMPT + user_prompt)
    tokens_out = estimate_tokens('{"risco_de_churn":"baixo","confianca":0.5,"acao":"n/a"}')
    cost = calculate_cost(tokens_in, tokens_out, settings)
    return tokens_in, tokens_out, cost
