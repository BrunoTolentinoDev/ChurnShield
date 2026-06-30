"""Testes do serviço de custo."""

from app.services.cost_service import calculate_cost, estimate_avoided_cost


class TestCostService:
    def test_calculate_cost(self) -> None:
        cost = calculate_cost(1000, 500)
        assert cost > 0

    def test_estimate_avoided_cost(self) -> None:
        tokens_in, tokens_out, cost = estimate_avoided_cost("Resumo", "Mensagem")
        assert tokens_in > 0
        assert tokens_out > 0
        assert cost > 0
