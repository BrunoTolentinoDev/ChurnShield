"""Testes das regras do Vigia."""

from app.layers.vigia.engine import run_vigia
from app.layers.vigia.rules import (
    check_delay,
    check_keywords,
    check_short_message,
)


class TestVigiaRules:
    def test_delay_triggered(self) -> None:
        result = check_delay(75.0)
        assert result.triggered is True
        assert result.name == "delay"

    def test_delay_not_triggered(self) -> None:
        result = check_delay(30.0)
        assert result.triggered is False

    def test_delay_none_not_triggered(self) -> None:
        result = check_delay(None)
        assert result.triggered is False

    def test_short_message_triggered(self) -> None:
        result = check_short_message("oi")
        assert result.triggered is True

    def test_short_message_not_triggered(self) -> None:
        result = check_short_message("Mensagem com tamanho adequado")
        assert result.triggered is False

    def test_keywords_cancelar(self) -> None:
        result = check_keywords("Quero cancelar meu plano")
        assert result.triggered is True

    def test_keywords_none(self) -> None:
        result = check_keywords("Obrigado pelo atendimento")
        assert result.triggered is False

    def test_engine_no_rules(self) -> None:
        result = run_vigia("Tudo funcionando perfeitamente, obrigado!", 10.0)
        assert result.any_triggered is False
        assert result.triggered_names == []

    def test_engine_multiple_rules(self) -> None:
        result = run_vigia("cancelar", 90.0)
        assert result.any_triggered is True
        assert "delay" in result.triggered_names
        assert "keywords" in result.triggered_names
