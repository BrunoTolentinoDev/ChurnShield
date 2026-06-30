"""Testes do Despertador."""

from app.layers.despertador.decider import decide
from app.layers.vigia.engine import run_vigia


class TestDespertador:
    def test_no_rules_skips_ai(self) -> None:
        vigia = run_vigia("Mensagem normal sem problemas aqui", 5.0)
        result = decide(vigia)
        assert result.should_call_ai is False
        assert result.economy_registered is True

    def test_rules_trigger_ai(self) -> None:
        vigia = run_vigia("Quero cancelar tudo", 10.0)
        result = decide(vigia)
        assert result.should_call_ai is True
        assert result.economy_registered is False
        assert "keywords" in result.reason
