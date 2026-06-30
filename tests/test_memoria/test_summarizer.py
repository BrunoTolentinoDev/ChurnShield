"""Testes da Memória Inteligente."""

from app.layers.memoria.summarizer import get_context_for_ai, update_summary


class TestMemoria:
    def test_first_message_creates_summary(self) -> None:
        result = update_summary("", ["Olá, preciso de ajuda"], 1)
        assert result.updated is True
        assert "ajuda" in result.summary

    def test_no_update_before_interval(self) -> None:
        result = update_summary("Resumo existente", ["msg2", "msg3"], 3)
        assert result.updated is False
        assert result.summary == "Resumo existente"

    def test_update_at_interval(self) -> None:
        messages = ["m1", "m2", "m3", "m4", "m5"]
        result = update_summary("Anterior", messages, 5)
        assert result.updated is True
        assert "Anterior" in result.summary
        assert "m5" in result.summary

    def test_context_for_ai_only_summary_and_last(self) -> None:
        ctx = get_context_for_ai("Resumo da conversa", "Última msg")
        assert ctx == {"resumo": "Resumo da conversa", "ultima_mensagem": "Última msg"}
        assert "historico_completo" not in ctx
