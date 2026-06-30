"""Cliente HTTP para a API DeepSeek."""

import json
import logging
import re
from dataclasses import dataclass

import httpx

from app.config import Settings, get_settings
from app.core.exceptions import AIClientError, AIResponseParseError
from app.layers.ia.prompts import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)


@dataclass
class AIAnalysisResult:
    """Resultado parseado da análise de IA."""

    risco_de_churn: str
    confianca: float
    acao: str
    tokens_input: int
    tokens_output: int
    raw_response: str


def estimate_tokens(text: str) -> int:
    """Estimativa simples de tokens (≈ 4 chars por token)."""
    return max(1, len(text) // 4)


class DeepSeekClient:
    """Cliente para API DeepSeek com fallback mock."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def analyze(self, resumo: str, ultima_mensagem: str) -> AIAnalysisResult:
        """Envia resumo + última mensagem e retorna análise estruturada."""
        if self.settings.use_mock_ai:
            return self._mock_analyze(resumo, ultima_mensagem)

        user_prompt = build_user_prompt(resumo, ultima_mensagem)
        payload = {
            "model": self.settings.deepseek_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        }

        headers = {
            "Authorization": f"Bearer {self.settings.deepseek_api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self.settings.deepseek_base_url.rstrip('/')}/chat/completions"

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            logger.error("Erro na API DeepSeek: %s", exc)
            raise AIClientError(f"Falha na API DeepSeek: {exc}") from exc

        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        tokens_in = usage.get("prompt_tokens", estimate_tokens(user_prompt))
        tokens_out = usage.get("completion_tokens", estimate_tokens(content))

        parsed = self._parse_json_response(content)
        return AIAnalysisResult(
            risco_de_churn=parsed["risco_de_churn"],
            confianca=float(parsed["confianca"]),
            acao=parsed["acao"],
            tokens_input=tokens_in,
            tokens_output=tokens_out,
            raw_response=content,
        )

    def _mock_analyze(self, resumo: str, ultima_mensagem: str) -> AIAnalysisResult:
        """Simula análise quando API não está disponível."""
        text = f"{resumo} {ultima_mensagem}".lower()
        high_risk_words = ("cancelar", "reembolso", "insatisfeito", "concorrente")
        medium_risk_words = ("caro", "depois")

        if any(w in text for w in high_risk_words):
            risco, confianca = "alto", 0.91
            acao = "Oferecer 15% de desconto e escalonar para retenção"
        elif any(w in text for w in medium_risk_words):
            risco, confianca = "medio", 0.72
            acao = "Esclarecer benefícios do plano e oferecer suporte prioritário"
        else:
            risco, confianca = "baixo", 0.55
            acao = "Manter atendimento padrão e monitorar"

        user_prompt = build_user_prompt(resumo, ultima_mensagem)
        raw = json.dumps(
            {"risco_de_churn": risco, "confianca": confianca, "acao": acao},
            ensure_ascii=False,
        )
        return AIAnalysisResult(
            risco_de_churn=risco,
            confianca=confianca,
            acao=acao,
            tokens_input=estimate_tokens(user_prompt),
            tokens_output=estimate_tokens(raw),
            raw_response=raw,
        )

    def _parse_json_response(self, content: str) -> dict:
        """Extrai e valida JSON da resposta da IA."""
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if not match:
                raise AIResponseParseError("Resposta da IA não contém JSON válido")
            data = json.loads(match.group())

        required = ("risco_de_churn", "confianca", "acao")
        for field in required:
            if field not in data:
                raise AIResponseParseError(f"Campo obrigatório ausente: {field}")

        return data
