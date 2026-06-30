"""Templates de prompt e schema JSON esperado da resposta."""

SYSTEM_PROMPT = """Você é um analisador de risco de churn em conversas de suporte.
Analise o resumo da conversa e a última mensagem do cliente.
Responda OBRIGATORIAMENTE em JSON válido, sem markdown, no formato:
{"risco_de_churn":"baixo|medio|alto","confianca":0.0,"acao":"sugestão de ação"}
"""


def build_user_prompt(resumo: str, ultima_mensagem: str) -> str:
    """Monta o prompt do usuário com contexto mínimo."""
    return (
        f"Resumo da conversa:\n{resumo}\n\n"
        f"Última mensagem do cliente:\n{ultima_mensagem}\n\n"
        "Analise o risco de churn e sugira uma ação."
    )
