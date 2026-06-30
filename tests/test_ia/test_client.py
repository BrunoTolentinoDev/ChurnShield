"""Testes do cliente de IA."""

import json

from app.config import Settings
from app.layers.ia.client import DeepSeekClient, estimate_tokens


class TestIAClient:
    def test_estimate_tokens(self) -> None:
        assert estimate_tokens("hello world") >= 1

    def test_mock_high_risk(self) -> None:
        settings = Settings(mock_ai=True, deepseek_api_key="")
        client = DeepSeekClient(settings)
        result = client.analyze("Cliente irritado", "Quero cancelar e pedir reembolso")
        assert result.risco_de_churn == "alto"
        assert result.confianca > 0.8
        assert "desconto" in result.acao.lower() or "retenção" in result.acao.lower()

    def test_mock_low_risk(self) -> None:
        settings = Settings(mock_ai=True, deepseek_api_key="")
        client = DeepSeekClient(settings)
        result = client.analyze("Tudo ok", "Obrigado pelo suporte")
        assert result.risco_de_churn == "baixo"

    def test_mock_returns_valid_json(self) -> None:
        settings = Settings(mock_ai=True, deepseek_api_key="")
        client = DeepSeekClient(settings)
        result = client.analyze("teste", "caro demais")
        parsed = json.loads(result.raw_response)
        assert "risco_de_churn" in parsed
        assert "confianca" in parsed
        assert "acao" in parsed
