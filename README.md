# ChurnShield

Analisa conversas de atendimento e tenta identificar quando o cliente está perto de cancelar.

A sacada do projeto: **não chamar IA em toda mensagem**. Primeiro passam regras simples em Python. Só se algo parecer estranho a DeepSeek entra pra analisar de verdade — com resumo da conversa, não o histórico inteiro.

Na prática tem um chat pra simular o cliente, um painel lateral mostrando o que rolou por trás (IA chamada? regras? custo? economia?) e um dashboard com métricas e histórico.

## Pipeline

Tudo fica em `app/layers/`:

| Etapa | O que faz |
|-------|-----------|
| Vigia | Regras locais: palavras-chave, demora na resposta, mensagem curta |
| Despertador | Decide se vale gastar com IA ou não |
| Memória | Mantém um resumo da conversa |
| IA | DeepSeek devolve risco, confiança e ação sugerida |
| Automação | Registra logs, custo e dispara resposta se o risco for alto |

## Stack

Python, FastAPI, SQLite, JavaScript (sem framework), DeepSeek API, Pytest.

## Como rodar

**Windows — um clique:** dê dois cliques em **`Iniciar ChurnShield.vbs`** (recomendado). Na primeira vez cria o venv, instala dependências e abre o navegador. Se o `.bat` abrir no editor em vez de rodar, use sempre o `.vbs`.

**Manual:**

```bash
git clone https://github.com/BrunoTolentinoDev/ChurnShield.git
cd ChurnShield

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env
uvicorn app.main:app --reload
```

No `.env`, coloque sua chave da DeepSeek ou use `MOCK_AI=true` pra testar sem gastar crédito.

Abre http://localhost:8000

## Testes

```bash
python -m pytest tests/ -v
```

Tem cobertura das regras, da decisão de chamar a IA, do client mock e dos endpoints.

## Estrutura

```
app/        API e lógica do pipeline
frontend/   chat + dashboard
tests/
```

O chat web é só demo. Separei a lógica do canal de entrada de propósito — a ideia é plugar WhatsApp ou webhook depois sem refatorar tudo.

## Ideias pra frente

- Deploy público
- Webhook WhatsApp
- Alerta quando risco for alto
- Gráficos no dashboard

---

Bruno Tolentino
